# 💊 AI Pharma Assistant

> A domain-grounded pharmaceutical intelligence system — search medicines, find cheaper substitutes, compare prices, and get AI-powered explanations. All backed by semantic search and a conversational LLM.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8?style=flat-square&logo=tailwindcss)
![LangChain](https://img.shields.io/badge/LangChain-latest-orange?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

---

## 🧠 What It Does

Many medicines share the same active ingredients but are sold under different brand names at vastly different prices. AI Pharma Assistant solves this by combining:

- **Semantic search** — find medicines from natural language queries
- **Composition-based retrieval** — identify true generic substitutes
- **Conversational LLM** — explain results in plain English
- **Agent-based routing** — intelligently decide which tool to use per query

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Medicine Search | Natural language queries like "What is Glycomet GP?" |
| 🔄 Substitute Finder | Composition-based alternatives, sorted by similarity |
| 💰 Price Comparison | "Which is the cheapest?" as a follow-up |
| 🧾 Markdown Responses | Structured, LLM-generated explanations |
| 🧠 Session Memory | SQLite-persistent conversation state with LRU cache |
| ⚡ Hybrid Search | Combines brand + composition FAISS indices (tunable alpha) |
| 🌊 SSE Streaming | Real-time, token-by-token text generation |
| 🎯 Pydantic Router | 100% deterministic tool routing via structured schemas |
| 🚀 HNSW Indexing | Optimized Hierarchical Navigable Small World vector search |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           Next.js Frontend          │
│  (Tailwind CSS + Framer Motion)     │
└────────────────┬────────────────────┘
                 │ HTTP POST /ask/stream (SSE)
                 ▼
┌─────────────────────────────────────┐
│         FastAPI Backend             │
│                                     │
│  ┌──────────┐    ┌───────────────┐  │
│  │  Agent   │───▶│ Pydantic      │  │
│  │  (Stream)│    │ Router        │  │
│  └──────────┘    └──────┬────────┘  │
│      ▲                  │           │
│      │                  ▼           │
│      │     ┌──────────────────────┐ │
│      │     │ search_tool          │ │
│  SQLiteDB  │ substitute_tool      │ │
│  (Persist) │ followup_tool        │ │
│      │     └────────────┬─────────┘ │
│      │                  ▼           │
│      │         ┌──────────────────┐  │
│      └─────────│    Retriever     │  │
│                │ (FAISS HNSW Graph)  │
│                └──────────────────┘  │
│                         │           │
│                         ▼           │
│                ┌──────────────────┐  │
│                │  LLM (Groq)      │  │
│                │  llama-3.1-8b    │  │
│                └──────────────────┘  │
└─────────────────────────────────────┘
```

---

## 📂 Project Structure

```
AIPharma/
├── app/
│   └── main.py               # FastAPI app, CORS, Sync and SSE Streaming /ask endpoints
├── core/
│   ├── agent.py              # PharmaAgent — orchestrates tool routing & token streams
│   ├── retrieval.py          # HNSW vector search, substitute matching & followup logic
│   ├── memory.py             # SQLite persistent session database with LRU Cache
│   ├── prompts.py            # Safety-disclaimer injected system prompts
│   ├── tools.py              # search, substitute, followup tool wrappers
│   └── config.py             # Settings (HNSW paths, parameters, thresholds)
├── Data/
│   ├── brand_search_hnsw.index       # HNSW brand search index
│   ├── composition_search_hnsw.index # HNSW composition search index
│   ├── sessions.db                   # SQLite persistent database file
│   └── medicine_metadata_dual.pkl    # Pandas DataFrame with medicine data
├── frontend/                 # Next.js web app
│   └── src/
│       ├── app/              # Next.js App Router pages + layout
│       ├── components/
│       │   ├── Chat/         # ChatWindow, MessageBubble, ChatInput
│       │   └── Layout/       # Header
│       ├── hooks/
│       │   └── useChat.ts    # Custom SSE stream hook updating real-time message state
│       ├── lib/
│       │   └── api.ts        # api fetch wrapper utilizing async generators
│       └── types/
│           └── chat.ts       # Message TypeScript types
├── notebooks/                # Data preprocessing & index building notebooks
├── build_hnsw_indices.py     # Offline HNSW FAISS graph index construction script
├── test_eval.py              # Standard evaluation script with UTF-8 printing
├── test_stream.py            # Async streaming generation test script
├── requirements.txt
└── pyproject.toml
```

---

## 📊 Performance & Data Metrics

### 1. Dataset Scale & Specifications
- **Total Cataloged Items**: `243,602` unique medicines
- **Unique Manufacturers**: `7,641` pharmaceutical companies
- **Price Range**: `₹0.00` to `₹396,725.00` (Mean: `₹262.11`, Median: `₹79.00`)
- **Metadata Footprint**: `~145 MB` DataFrame on disk, loading into `~320 MB` RAM space

### 2. FAISS HNSW Indices
- **Vector Count**: `243,602` vectors per index
- **Dimensions**: `384` dimensions (`all-MiniLM-L6-v2`)
- **File Size**: `420.07 MB` per index (`brand_search_hnsw.index` / `composition_search_hnsw.index`)

### 3. Empirical Latencies
- **FAISS HNSW Vector Query Search**: `~74.9 ms` (reduced from `~227 ms` in standard flat search)
- **Groq Intent Routing**: `~180 - 250 ms`
- **Groq LLM Streaming Token Delay (Time-to-First-Token)**: `~150 ms`
- **End-to-End SSE API Chunk Delivery**: `~550 - 900 ms`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Groq API key](https://console.groq.com/)

### 1. Clone the repository

```bash
git clone https://github.com/PrathmeshJugati/ai-pharma-assistant.git
cd ai-pharma-assistant
```

### 2. Set up the Python backend

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Build HNSW FAISS Indices (One-time Setup)

Convert the standard flat indices to HNSW vector graph search indices:
```bash
python build_hnsw_indices.py
```

### 5. Run the backend uvicorn server

```bash
fastapi dev app/main.py
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### 6. Set up and run the frontend

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

```bash
npm run dev
# App available at http://localhost:3000
```

---

## 🔌 API Reference

### `POST /ask/stream` (Streaming response)

Query the assistant and receive token chunk streams in real-time.

**Request Body:**
```json
{
  "query": "Give me substitutes for Glycomet GP",
  "session_id": "uuid-string-here"
}
```

**Response:**
Server-Sent Events text stream.

---

### `POST /ask` (Synchronous response)

**Request Body:**
```json
{
  "query": "What is Glycomet GP?",
  "session_id": "uuid-string-here"
}
```

**Response:**
```json
{
  "response": "Glycomet GP is a combination medicine containing Glimepiride and Metformin..."
}
```

---

## ⚙️ Configuration

All tuneable parameters live in `core/config.py`: 

| Parameter | Default | Description |
|---|---|---|
| `LLM_MODEL` | `llama-3.1-8b-instant` | Groq model to use |
| `LLM_TEMPERATURE` | `0.2` | LLM output randomness |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | SentenceTransformer model |
| `TOP_K` | `5` | Number of retrieval results |
| `ALPHA` | `0.9` | Brand vs composition weight (hybrid search) |
| `ANCHOR_THRESHOLD` | `0.54` | Minimum similarity for substitute anchor |
| `USE_HNSW_IF_AVAILABLE` | `True` | Automatically load HNSW indices if built |

---

## 🧩 How It Works

1. **Query arrives** at `POST /ask/stream` with an optional `session_id`.
2. **`choose_tool()`** — uses Pydantic structured output formatting to select one of `search_tool`, `substitute_tool`, or `followup_tool`.
3. **Tool executes:**
   - `search_tool` → hybrid HNSW search (brand + composition) returning name, composition, price, and medical description
   - `substitute_tool` → brand anchor search followed by composition-based alternatives
   - `followup_tool` → queries SQLite session database and fetches generic substitute fallbacks if not previously retrieved
4. **`build_prompt_new()`** — constructs role-specific system messages enforcing medical safety disclaimers.
5. **LLM generates** explanation stream chunk-by-chunk using Groq.

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [LangChain](https://langchain.com/) — LLM orchestration
- [Groq](https://groq.com/) — Ultra-fast LLM inference (`llama-3.1-8b-instant`)
- [FAISS](https://github.com/facebookresearch/faiss) — Vector similarity search (HNSW Graph support)
- [SentenceTransformers](https://www.sbert.net/) — `all-MiniLM-L6-v2` embeddings
- [pandas](https://pandas.pydata.org/) — Medicine metadata store

**Frontend**
- [Next.js 15](https://nextjs.org/) — React framework (App Router)
- [Tailwind CSS](https://tailwindcss.com/) — Utility-first styling
- [Framer Motion](https://www.framer.com/motion/) — Micro-animations
- [React Markdown](https://github.com/remarkjs/react-markdown) — LLM response rendering
- [Lucide React](https://lucide.dev/) — Icons

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- Medicine dataset sourced from [Github](https://github.com/junioralive/Indian-Medicine-Dataset.git)
- Powered by [Groq](https://groq.com/) for blazing-fast LLM inference.
- FAISS by [Meta AI Research](https://github.com/facebookresearch/faiss).
