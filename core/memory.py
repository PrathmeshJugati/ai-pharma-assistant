import json
import sqlite3
from collections import OrderedDict
from core.config import settings

class ConversationMemory:

    MAX_SESSIONS = 500  # Evict oldest session from RAM cache beyond this limit

    def __init__(self, db_path=settings.SESSION_DB_PATH):
        self.sessions: OrderedDict = OrderedDict()
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS session_memory (
                        session_id TEXT PRIMARY KEY,
                        last_intent TEXT,
                        last_mode TEXT,
                        last_results TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        except Exception as e:
            print(f"[Memory DB Warn] Could not initialize SQLite memory store: {e}")

    def _load_from_db(self, session_id: str) -> dict | None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT last_intent, last_mode, last_results FROM session_memory WHERE session_id = ?",
                    (session_id,)
                )
                row = cursor.fetchone()
                if row:
                    last_intent, last_mode, last_results_raw = row
                    last_results = json.loads(last_results_raw) if last_results_raw else None
                    return {
                        "last_intent": last_intent,
                        "last_mode": last_mode,
                        "last_results": last_results
                    }
        except Exception as e:
            print(f"[Memory DB Error] Failed to load session {session_id}: {e}")
        return None

    def _save_to_db(self, session_id: str, state: dict):
        try:
            with sqlite3.connect(self.db_path) as conn:
                last_results_json = json.dumps(state.get("last_results")) if state.get("last_results") else None
                conn.execute("""
                    INSERT INTO session_memory (session_id, last_intent, last_mode, last_results, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(session_id) DO UPDATE SET
                        last_intent = excluded.last_intent,
                        last_mode = excluded.last_mode,
                        last_results = excluded.last_results,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    session_id,
                    state.get("last_intent"),
                    state.get("last_mode"),
                    last_results_json
                ))
                conn.commit()
        except Exception as e:
            print(f"[Memory DB Error] Failed to save session {session_id}: {e}")

    def _get_or_create_session(self, session_id: str) -> dict:
        if session_id not in self.sessions:
            # Try to load from SQLite DB first
            db_state = self._load_from_db(session_id)
            if db_state:
                state = db_state
            else:
                state = {
                    "last_intent": None,
                    "last_mode": None,
                    "last_results": None
                }

            if len(self.sessions) >= self.MAX_SESSIONS:
                self.sessions.popitem(last=False)  # evict the oldest from RAM

            self.sessions[session_id] = state
        else:
            self.sessions.move_to_end(session_id)

        return self.sessions[session_id]

    def update(self, session_id: str = "default", intent=None, mode=None, results=None):
        state = self._get_or_create_session(session_id)

        if intent:
            state["last_intent"] = intent
        if mode:
            state["last_mode"] = mode
        if results:
            state["last_results"] = results

        # Persist to SQLite
        self._save_to_db(session_id, state)

    def get(self, session_id: str = "default") -> dict:
        return self._get_or_create_session(session_id)