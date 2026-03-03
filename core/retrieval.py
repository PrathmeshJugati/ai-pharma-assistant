import os
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from core.config import settings

class Retriever:
    
    def __init__(self, encoder=settings.EMBEDDING_MODEL):
        self.model = SentenceTransformer(encoder)
        self.brand_index = faiss.read_index(str(settings.BRAND_INDEX_PATH))
        self.composition_index = faiss.read_index(str(settings.COMPOSITION_INDEX_PATH))
        self.dt = pd.read_pickle(settings.METADATA_PATH)

    def format_medicine_results(self,df_slice):

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
    
    def find_anchor(self,query):

        q = self.model.encode(
        [query],
        normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.brand_index.search(q, 1)

        best_score = float(scores[0][0])
        best_idx = int(indices[0][0])
        print(best_score)
        # If similarity is weak, do NOT treat as anchor
        if best_score < settings.ANCHOR_THRESHOLD:
            return None

        return self.dt.iloc[best_idx]
    

    def hybrid_search(self,query, top_k=5, alpha=0.4):
        """
        alpha controls importance:
        alpha small → composition dominates
        alpha large → brand dominates
        """

        query_embedding = self.model.encode([query]).astype("float32")
        faiss.normalize_L2(query_embedding)

        brand_scores, brand_ids = self.brand_index.search(query_embedding, top_k)
        comp_scores, comp_ids = self.composition_index.search(query_embedding, top_k)

        scores = {}

        # brand contribution
        for score, idx in zip(brand_scores[0], brand_ids[0]):
            scores[idx] = scores.get(idx, 0) + alpha * score

        # composition contribution
        for score, idx in zip(comp_scores[0], comp_ids[0]):
            scores[idx] = scores.get(idx, 0) + (1 - alpha) * score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        final_indices = [idx for idx, _ in ranked[:top_k]]

        df_slice =  self.dt.iloc[final_indices][
            ["name", "composition", "manufacturer_name", "price"]
        ]

        return self.format_medicine_results(df_slice)
    

    def find_substitute(self,query, top_k=5):
        """
        Find substitutes based primarily on composition similarity.

        alpha:
            small  → composition dominates
            large  → brand similarity dominates (optional future use)
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
                continue  # remove same medicine

            scores[idx] = float(score)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        final_indices = [idx for idx, _ in ranked[:top_k]]

        df_slice =  self.dt.iloc[final_indices][
            ["name", "composition", "manufacturer_name", "price"]
        ]

        return self.format_medicine_results(df_slice)
    

    def handle_followup(self, query, memory_state):

        results = memory_state["last_results"]

        if not results:
            return None

        q = query.lower()

        if "cheap" in q or "cheapest" in q:

            cheapest = min(results, key=lambda x: x["price"])

            return {
                "followup_type": "followup",
                "action": "cheapest",
                "result": cheapest,
                "results": results
            }
        
        if "compare" in q and len(results) >= 2:

            m1, m2 = results[0], results[1]

            return {
                "followup_type": "comparison",
                "medicine_1": m1,
                "medicine_2": m2,
                "price_difference":
                    abs(m1["price"] - m2["price"])
            }