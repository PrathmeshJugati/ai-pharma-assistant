import os
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from core.config import settings

class Retriever:
    
    # Expanded keyword sets for more natural language coverage
    _CHEAP_KW = {"cheap", "cheapest", "affordable", "lowest", "budget", "inexpensive", "economical", "least expensive"}
    _COMPARE_KW = {"compare", "comparison", "difference", "vs", "versus", "better", "contrast", "which is better"}

    def __init__(self, encoder=settings.EMBEDDING_MODEL):
        self.model = SentenceTransformer(encoder)
        self.brand_index = faiss.read_index(str(settings.BRAND_INDEX_PATH))
        self.composition_index = faiss.read_index(str(settings.COMPOSITION_INDEX_PATH))
        self.dt = pd.read_pickle(settings.METADATA_PATH)

    def format_medicine_results(self, df_slice):
        results = []
        for _, row in df_slice.iterrows():
            results.append({
                "name": row["name"],
                "composition": row["composition"],
                "manufacturer": row["manufacturer_name"],
                "price": float(row["price"])
            })
        return {
            "type": "medicine_list",
            "results": results
        }

    def find_anchor(self, query):
        """
        Find the best-matching medicine anchor for a given query using the brand index.
        Returns None if the similarity score is below the configured threshold.
        """
        q = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.brand_index.search(q, 1)

        best_score = float(scores[0][0])
        best_idx = int(indices[0][0])
        print(f"[Anchor] best_score={best_score:.3f}")

        if best_score < settings.ANCHOR_THRESHOLD:
            return None

        return self.dt.iloc[best_idx]

    def hybrid_search(self, query, top_k=5, alpha=0.4):
        """
        Hybrid FAISS search combining brand and composition indices.
        alpha → 1.0: brand dominates | alpha → 0.0: composition dominates
        """
        query_embedding = self.model.encode([query], normalize_embeddings=True).astype("float32")

        brand_scores, brand_ids = self.brand_index.search(query_embedding, top_k)
        comp_scores, comp_ids = self.composition_index.search(query_embedding, top_k)

        scores = {}

        for score, idx in zip(brand_scores[0], brand_ids[0]):
            scores[idx] = scores.get(idx, 0) + alpha * score

        for score, idx in zip(comp_scores[0], comp_ids[0]):
            scores[idx] = scores.get(idx, 0) + (1 - alpha) * score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        final_indices = [idx for idx, _ in ranked[:top_k]]

        df_slice = self.dt.iloc[final_indices][
            ["name", "composition", "manufacturer_name", "price"]
        ]
        return self.format_medicine_results(df_slice)

    def find_substitute(self, query, top_k=5):
        """
        Find substitutes by:
        1. Finding the anchor medicine via brand similarity.
        2. Encoding its composition to find composition-similar alternatives.
        """
        anchor = self.find_anchor(query)

        if anchor is None:
            return None

        anchor_idx = anchor.name
        anchor_composition = anchor["composition"]

        comp_text = f"active ingredients {anchor_composition} pharmaceutical drug composition"

        comp_emb = self.model.encode(
            [comp_text],
            normalize_embeddings=True
        ).astype("float32")

        comp_scores, comp_ids = self.composition_index.search(comp_emb, top_k + 1)

        scores = {}
        for score, idx in zip(comp_scores[0], comp_ids[0]):
            if idx == anchor_idx:
                continue  # exclude the anchor medicine itself
            scores[idx] = float(score)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        final_indices = [idx for idx, _ in ranked[:top_k]]

        df_slice = self.dt.iloc[final_indices][
            ["name", "composition", "manufacturer_name", "price"]
        ]
        return self.format_medicine_results(df_slice)

    def handle_followup(self, query, memory_state):
        """
        Handle follow-up queries using the results already in session memory.
        Supports: cheapest, comparison, and general context re-surfacing.
        """
        results = memory_state["last_results"]

        if not results:
            return None

        q = query.lower()

        # Check for cheapest-related intent
        if any(kw in q for kw in self._CHEAP_KW):
            cheapest = min(results, key=lambda x: x["price"])
            return {
                "followup_type": "followup",
                "action": "cheapest",
                "result": cheapest,
                "results": results
            }

        # Check for comparison intent
        if any(kw in q for kw in self._COMPARE_KW) and len(results) >= 2:
            m1, m2 = results[0], results[1]
            return {
                "followup_type": "comparison",
                "medicine_1": m1,
                "medicine_2": m2,
                "price_difference": abs(m1["price"] - m2["price"])
            }

        # Fallback: re-surface prior results for the LLM to answer from context
        return {
            "followup_type": "general",
            "results": results
        }