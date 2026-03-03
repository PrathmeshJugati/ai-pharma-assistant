# AI Pharma Assistant — Next.js MVP Walkthrough

## What Was Built

A professional, full-stack Next.js frontend for the existing FastAPI + Langchain AI Pharma backend, with the backend also patched for multi-user session support.

## File Structure

```
AIPharma/
├── app/
│   └── main.py           ← [MODIFIED] Added CORS + session_id
├── core/
│   ├── agent.py          ← [MODIFIED] session_id threading
│   ├── memory.py         ← [MODIFIED] Per-session dict-based memory
│   └── tools.py          ← [MODIFIED] session_id in followup_tool
└── frontend/             ← [NEW] Next.js App
    ├── .env.local
    └── src/
        ├── app/
        │   ├── layout.tsx       ← SEO metadata, font setup
        │   ├── page.tsx         ← Main page assembly
        │   └── globals.css      ← Tailwind + typography plugin
        ├── components/
        │   ├── Chat/
        │   │   ├── ChatWindow.tsx      ← Scrollable message list
        │   │   ├── MessageBubble.tsx   ← Framer Motion animated bubbles
        │   │   ├── ChatInput.tsx       ← Glassmorphism textarea + send
        │   │   ├── TypingIndicator.tsx ← Animated 3-dot loader
        │   │   └── EmptyState.tsx      ← Welcome screen + suggestion chips
        │   └── Layout/
        │       └── Header.tsx          ← App header + New Chat button
        ├── hooks/
        │   └── useChat.ts       ← Session ID, messages, API calls
        ├── lib/
        │   └── api.ts           ← Fetch wrapper for FastAPI
        └── types/
            └── chat.ts          ← Message type definitions
```

## Key Technical Decisions

- **Session-based memory**: Each browser session generates a UUID via [useChat.ts](file:///c:/ML%20Projects/AIPharma/frontend/src/hooks/useChat.ts) → sent as `session_id` to backend. Backend [ConversationMemory](file:///c:/ML%20Projects/AIPharma/core/memory.py#1-29) is now a dictionary keyed by session ID.
- **Glassmorphism input bar**: Uses `backdrop-blur-md bg-white/70 border border-slate-200`.
- **Framer Motion**: Each message bubble uses `initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}`.
- **Markdown rendering**: `react-markdown` + `remark-gfm` + `@tailwindcss/typography` renders bullet points and bold text from AI responses.

## Screenshots

### Empty State
![Empty State — Welcome screen with suggestion chips](C:\Users\prath\.gemini\antigravity\brain\9872925e-bd80-469d-9a2f-f6a4274112f9\initial_empty_state_1772535783103.png)

### Active Chat (Glycomet GP query)
![Chat response — Markdown-rendered drug info with pricing](C:\Users\prath\.gemini\antigravity\brain\9872925e-bd80-469d-9a2f-f6a4274112f9\chat_state_response_1772535809621.png)

## How To Run

**Terminal 1 — Backend:**
```bash
fastapi dev app/main.py
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open **http://localhost:3000**.
