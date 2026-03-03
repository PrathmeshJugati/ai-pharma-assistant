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
| 🧠 Session Memory | Follow-up questions retain context per user session |
| ⚡ Hybrid Search | Combines brand + composition FAISS indices (tunable alpha) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           Next.js Frontend          │
│  (Tailwind CSS + Framer Motion)     │
└────────────────┬────────────────────┘
                 │ HTTP POST /ask
                 ▼
┌─────────────────────────────────────┐
│         FastAPI Backend             │
│                                     │
│  ┌──────────┐    ┌───────────────┐  │
│  │  Agent   │───▶│ Tool Router   │  │
│  └──────────┘    └──────┬────────┘  │
│                         │           │
│          ┌──────────────┼──────────┐│
│          ▼              ▼          ▼│
│    search_tool   substitute_tool  followup_tool
│          │              │          │ │
│          └──────────────┼──────────┘│
│                         ▼           │
│               ┌──────────────────┐  │
│               │    Retriever     │  │
│               │ (FAISS + SentTX) │  │
│               └──────────────────┘  │
│                         │           │
│                         ▼           │
│               ┌──────────────────┐  │
│               │  LLM (Groq)      │  │
│               │  llama-3.1-8b    │  │
│               └──────────────────┘  │
└─────────────────────────────────────┘
```

---

## � Project Structure

```
AIPharma/
├── app/
│   └── main.py               # FastAPI app, CORS, /ask endpoint
├── core/
│   ├── agent.py              # PharmaAgent — orchestrates tool routing + LLM
│   ├── retrieval.py          # FAISS hybrid search, substitute finder, followups
│   ├── memory.py             # Per-session LRU conversation memory
│   ├── prompts.py            # System prompts for agent + response generation
│   ├── tools.py              # search, substitute, followup tool wrappers
│   └── config.py             # Settings (model names, paths, thresholds)
├── Data/
│   ├── brand_search.index    # FAISS brand index
│   ├── composition_search.index  # FAISS composition index
│   └── medicine_metadata_dual.pkl  # Pandas DataFrame with medicine data
├── frontend/                 # Next.js web app
│   └── src/
│       ├── app/              # Next.js App Router pages + layout
│       ├── components/
│       │   ├── Chat/         # ChatWindow, MessageBubble, ChatInput, TypingIndicator, EmptyState
│       │   └── Layout/       # Header
│       ├── hooks/
│       │   └── useChat.ts    # Session UUID, message state, API integration
│       ├── lib/
│       │   └── api.ts        # Fetch wrapper for FastAPI /ask endpoint
│       └── types/
│           └── chat.ts       # Message TypeScript types
├── notebooks/                # Data preprocessing & index building notebooks
├── test_eval.py              # Manual evaluation script
├── requirements.txt
└── pyproject.toml
```

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
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the backend

```bash
fastapi dev app/main.py
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### 5. Set up and run the frontend

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

### `POST /ask`

Query the pharmaceutical assistant.

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

**Notes:**
- `session_id` is optional (defaults to `"default"`)
- Send the same `session_id` across turns to maintain follow-up context

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

---

## 🧩 How It Works

1. **Query arrives** at `POST /ask` with an optional `session_id`.
2. **`choose_tool()`** — the LLM reads the query and picks one of `search_tool`, `substitute_tool`, or `followup_tool`.
3. **Tool executes:**
   - `search_tool` → hybrid FAISS search (brand + composition)
   - `substitute_tool` → anchor search → composition-based alternatives
   - `followup_tool` → uses session memory to answer follow-ups (cheapest, compare, etc.)
4. **`build_prompt_new()`** — wraps the retrieved data + query into a role-specific LLM prompt.
5. **LLM generates** a natural language explanation grounded strictly in the retrieved data.

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [LangChain](https://langchain.com/) — LLM orchestration
- [Groq](https://groq.com/) — Ultra-fast LLM inference (`llama-3.1-8b-instant`)
- [FAISS](https://github.com/facebookresearch/faiss) — Vector similarity search
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
