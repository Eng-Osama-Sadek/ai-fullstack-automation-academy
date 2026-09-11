class AITutorEngine:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def ask_tutor(self, prompt: str, context: str) -> str:
        return f"AITutor [Track: {context}]: Processed prompt -> '{prompt}'"
