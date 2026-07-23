# build_hnsw_indices.py

import os
import time
import faiss
import numpy as np
from core.config import settings

def convert_flat_to_hnsw(flat_index_path, hnsw_output_path, M=32, ef_construction=64, ef_search=32):
    print(f"Loading Flat index from: {flat_index_path}")
    flat_index = faiss.read_index(str(flat_index_path))
    
    ntotal = flat_index.ntotal
    dim = flat_index.d
    print(f"Index contains {ntotal} vectors of dimension {dim}")

    # Re-extract vectors
    print("Re-extracting vectors from Flat index...")
    t0 = time.time()
    vectors = flat_index.reconstruct_n(0, ntotal)
    print(f"Extracted in {time.time() - t0:.2f}s, matrix shape: {vectors.shape}")

    print(f"Constructing IndexHNSWFlat (M={M}, efConstruction={ef_construction})...")
    hnsw_index = faiss.IndexHNSWFlat(dim, M, faiss.METRIC_INNER_PRODUCT)
    hnsw_index.hnsw.efConstruction = ef_construction
    hnsw_index.hnsw.efSearch = ef_search

    t0 = time.time()
    hnsw_index.add(vectors)
    print(f"Added {ntotal} vectors to HNSW index in {time.time() - t0:.2f}s")

    print(f"Saving HNSW index to: {hnsw_output_path}")
    faiss.write_index(hnsw_index, str(hnsw_output_path))
    print(f"Saved successfully ({os.path.getsize(hnsw_output_path) / (1024*1024):.2f} MB)")

def main():
    print("=" * 60)
    print("Building HNSW Indices for AI Pharma Assistant")
    print("=" * 60)

    # 1. Brand Index
    convert_flat_to_hnsw(
        settings.BRAND_INDEX_PATH,
        settings.HNSW_BRAND_INDEX_PATH
    )

    print("-" * 60)

    # 2. Composition Index
    convert_flat_to_hnsw(
        settings.COMPOSITION_INDEX_PATH,
        settings.HNSW_COMPOSITION_INDEX_PATH
    )

    print("=" * 60)
    print("HNSW Index construction complete!")

if __name__ == "__main__":
    main()
