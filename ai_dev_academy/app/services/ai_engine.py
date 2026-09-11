import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class AITutorEngine:
    def __init__(self, api_key: str | None = None):
        self.key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        self.client = genai.Client(api_key=self.key)

    def ask_tutor(self, prompt: str, context: str) -> str:
        sys_instruction = (
            f"You are an expert AI software tutor specializing in {context}.\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "1. Always output clean, readable, and structured responses.\n"
            "2. Wrap ALL Python code strictly inside markdown code blocks using ```python with proper line breaks (never output single-line compressed code).\n"
            "3. Ensure distinct separation between explanations, scenario text, and code snippets."
        )
        
        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={"system_instruction": sys_instruction}
        )
        return response.text