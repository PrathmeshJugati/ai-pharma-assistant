class ConversationMemory:

    def __init__(self):
        self.sessions = {}

    def _get_or_create_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "last_intent": None,
                "last_mode": None,
                "last_results": None
            }
        return self.sessions[session_id]

    def update(self, session_id: str = "default", intent=None, mode=None, results=None):
        state = self._get_or_create_session(session_id)

        if intent:
            state["last_intent"] = intent

        if mode:
            state["last_mode"] = mode

        if results:
            state["last_results"] = results

    def get(self, session_id: str = "default"):
        return self._get_or_create_session(session_id)