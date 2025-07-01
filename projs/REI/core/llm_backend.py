import json5
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
# Imports

load_dotenv()

class LLMBackend:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt_parts, temp: float, top_p: float, top_k: float, sys_inst: str) -> str:
        raise NotImplementedError("Not implemented in base class")


class FakeGeminiBackend(LLMBackend):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.resp_count = 0
        self.responses = [
            """{
  "thought": "Окей, я определил критерии. Теперь мне нужно найти актуальную информацию о популярности языков программирования в 2025 году. Для этого лучше всего использовать поиск.",
  "tool_name": "GoogleSearch",
  "tool_query": "most popular programming languages 2025",
  "confidence": 0.95,
  "nextThoughtsNeeded": true
}""",
            """{
  "thought": "Я проанализировал результаты поиска. Python лидирует в сфере AI, JavaScript в вебе, а Rust набирает популярность в системном программировании. Теперь я готов синтезировать финальный ответ для пользователя.",
  "tool_name": null,
  "tool_query": null,
  "confidence": 1.0,
  "nextThoughtsNeeded": false
}""",
        ]

    def generate(
        self, prompt_parts, temp: float, top_p: float, top_k: float, sys_inst: str
    ) -> str:
        print("Fake Gemini backend Вызван")
        if self.resp_count < len(self.responses):
            response = self.responses[self.resp_count]
            self.resp_count += 1
            return response

        else:
            return """{
                "thought": "Готово!",
                "nextThoughtNeeded": false,
                }"""

class GeminiBackend(LLMBackend):
    def __init__(self):
        api_key = os.getenv("GEMINI_BACKEND_API")
        if not api_key:
            raise ValueError("--- GEMINI_BACKEND_API NOT FOUND ---")

        self.client = genai.Client(api_key=api_key)
    print("--- GEMINI BACKEND INITIALIZED ---")
    
    async def generate(self, prompt_parts, temp: float, top_p: float, top_k: float, sys_inst: str) -> str:
        print("--- GEMINI BACKEND GENERATE START ---")
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_parts,
                config=types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    top_k= top_k,
                    top_p = top_p,
                    temperature=temp,
                )
            )
            return response.text
        except Exception as e:
            print("--- GEMINI BACKEND GENERATION FAULT")
            print(f"--- EXCEPTION IS {e} ---")
