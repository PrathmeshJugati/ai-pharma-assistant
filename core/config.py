# config.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:


    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "llama-3.1-8b-instant"
    LLM_TEMPERATURE = 0.2


    TOP_K = 5
    ALPHA = 0.9
    ANCHOR_THRESHOLD = 0.540


    DATA_DIR = BASE_DIR / "Data"
    BRAND_INDEX_PATH = DATA_DIR / "brand_search.index"
    COMPOSITION_INDEX_PATH = DATA_DIR / "composition_search.index"
    HNSW_BRAND_INDEX_PATH = DATA_DIR / "brand_search_hnsw.index"
    HNSW_COMPOSITION_INDEX_PATH = DATA_DIR / "composition_search_hnsw.index"
    METADATA_PATH = DATA_DIR / "medicine_metadata_dual.pkl"
    SESSION_DB_PATH = DATA_DIR / "sessions.db"

    USE_HNSW_IF_AVAILABLE = True

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

settings = Settings()