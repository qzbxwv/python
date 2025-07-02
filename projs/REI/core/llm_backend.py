import json5
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
from google.genai.types import HttpOptions
# Imports

load_dotenv()

class LLMBackend:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, prompt_parts, temp : float, sys_inst: str) -> str:
        raise NotImplementedError("Not implemented in base class")

class GeminiBackend(LLMBackend):
    def __init__(self):
        api_key = os.getenv("GEMINI_BACKEND_API")
        if not api_key:
            raise ValueError("--- GEMINI_BACKEND_API NOT FOUND ---")

        self.client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version="v1"))
    print("--- GEMINI BACKEND INITIALIZED SUCCESS ---")
    
    async def generate(self, prompt_parts, temp: float, sys_inst: str) -> str:
        print("--- GEMINI BACKEND GENERATE START ---")
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-2.5-flash",
                #config=types.GenerateContentConfig(
                #    system_instruction=sys_inst,
                #    temperature=temp,
                # ),
                contents=prompt_parts,
            )
            print("--- GEMINI BACKEND RETURN RESPONSE ---")
            return f"Мысль: {response.text}"
        
        except Exception as e:
            print("--- GEMINI BACKEND GENERATION FAULT")
            print(f"--- EXCEPTION IS {e} ---")
            return "Excepcion"
