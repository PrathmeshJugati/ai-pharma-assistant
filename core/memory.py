from collections import OrderedDict

class ConversationMemory:

    MAX_SESSIONS = 500  # Evict oldest session beyond this limit (prevent memory leak)

    def __init__(self):
        self.sessions: OrderedDict = OrderedDict()

    def _get_or_create_session(self, session_id: str) -> dict:
        if session_id not in self.sessions:
            if len(self.sessions) >= self.MAX_SESSIONS:
                self.sessions.popitem(last=False)  # evict the oldest (LRU style)
            self.sessions[session_id] = {
                "last_intent": None,
                "last_mode": None,
                "last_results": None
            }
        # Move to end on access (most recently used)
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

    def get(self, session_id: str = "default") -> dict:
        return self._get_or_create_session(session_id)