# AI Pharma Assistant - Next.js MVP Design & Implementation Plan

This document outlines the Minimum Viable Product (MVP) design and architecture for the Next.js frontend of the AI Pharma Assistant. The goal is to create a professional, highly responsive, and visually stunning web application that interfaces with the existing FastAPI backend.

## 1. UI/UX Design Strategy (The "Proper" Setup)

We will use a premium technology stack to ensure a modern look and feel:
- **Framework:** Next.js 15 (App Router)
- **Styling:** Tailwind CSS v3 for utility-first responsive design.
- **Animations:** Framer Motion for liquid-smooth micro-animations (e.g., messages sliding in, intelligent typing indicators).
- **UI Primitives:** Shadcn UI + Radix UI for accessible, unstyled core components that we customize heavily.
- **Icons:** Lucide React for consistent, crisp vector icons.
- **Markdown:** `react-markdown` to properly format the AI's structured responses (bolding, lists).

### Visual Identity
- **Theme:** Clean, clinical "Light Mode" default with subtle healthcare accents (Soft teal/blue gradients). Optional glassmorphism on floating elements.
- **Typography:** `Inter` or `Geist` (Next.js default) for crystal-clear readability.
- **Layout:** A centered, focused chat interface (similar to ChatGPT or Claude), but tailored for quick drug queries.

---

## 2. Component Architecture

The application will be divided into modular, reusable components inside `frontend/src/components/`:

### 2.1 Core Layout (`components/Layout/`)
- `AppLayout`: The main shell containing the header and the main content area.
- `Header`: Contains the App Logo/Title ("AI Pharma Assistant"), a "New Chat" button to reset the session, and an optional theme toggle.

### 2.2 Chat Interface (`components/Chat/`)
- `ChatWindow`: The scrollable container that renders the list of messages. It handles auto-scrolling to the bottom when new messages arrive.
- `MessageBubble`: A polymorphic component that renders differently based on the sender (`user` vs [assistant](file:///c:/ML%20Projects/AIPharma/core/agent.py#58-69)).
  - **User Bubble:** Aligned right, solid subtle background.
  - **Assistant Bubble:** Aligned left, distinct background, supports markdown rendering, includes a "bot" avatar icon.
- `ChatInput`: The floating or sticky text area at the bottom.
  - Multi-line support (auto-expanding textarea).
  - Submit button that is disabled while loading.
  - Enter-to-submit logic (Shift+Enter for new line).
- `TypingIndicator`: A Framer Motion powered animated "three dots" loader shown while waiting for the FastAPI response.

### 2.3 UI Primitives (`components/ui/` - Shadcn)
- `Button`, `Input`, `Textarea`, `ScrollArea`, `Avatar`.

---

## 3. State Management & Data Flow

### 3.1 Client-Side State (`hooks/useChat.ts`)
We will build a custom React hook `useChat` to encapsulate all chat logic:
- **State variables:**
  - `messages`: Array of `{ role: 'user' | 'assistant', content: string, id: string }`.
  - `isLoading`: Boolean to show the typing indicator and disable input.
  - `input`: The current value of the textarea.
  - `sessionId`: A unique UUID generated on the client when a new chat starts, sent to the backend to maintain context.

### 3.2 API Integration (`lib/api.ts`)
Service functions to communicate with the FastAPI backend:
- `sendMessage(query: string, sessionId: string)`: 
  - Makes a `POST` request to `http://localhost:8000/ask`.
  - Payload: `{ "query": query, "session_id": sessionId }`.
  - Returns the [QueryResponse](file:///c:/ML%20Projects/AIPharma/app/main.py#43-45).

---

## 4. Implementation Steps (The Plan)

This is the exact sequence of technical steps we will execute:

### Phase 1: Project Initialization
1.  **Create Next.js App:** 
    `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"`
2.  **Install Dependencies:** 
    `npm install framer-motion lucide-react react-markdown uuid`
    `npx shadcn@latest init` 
3.  **Setup Shadcn Components:** 
    Install required primitives (e.g., `npx shadcn@latest add button textarea scroll-area avatar`).

### Phase 2: Core Logic Build
4.  **API Client Layer:** Create `frontend/src/lib/api.ts` to define the Fetch calls to the Python backend.
5.  **State Hook:** Create `frontend/src/hooks/useChat.ts` to manage the `messages` array, `sessionId` generation (using `uuid`), and the `sendMessage` logic.

### Phase 3: UI Construction
6.  **Build Primitives:** Create the `MessageBubble`, `TypingIndicator`, and `ChatInput` components in `frontend/src/components/Chat/`.
    - Apply Framer Motion to make bubbles slide up and fade in (`initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}`).
7.  **Assemble Chat Window:** Combine all components into the main page (`frontend/src/app/page.tsx`). Implement auto-scrolling logic using a React `ref`.
8.  **Styling Polish:** Refine the Tailwind classes for a premium look (gradients, shadows, responsive padding).

### Phase 4: Integration & Testing
9.  **CORS Configuration:** Ensure `FastAPI` in [app/main.py](file:///c:/ML%20Projects/AIPharma/app/main.py) has `CORSMiddleware` configured to allow requests from `http://localhost:3000`.
10. **End-to-End Test:** Run both servers locally, test prompt submission, check markdown formatting of the response, and verify that follow-up questions work correctly using the newly implemented backend `session_id`.
