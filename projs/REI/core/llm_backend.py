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

    async def generate(self, prompt_parts, temp : float, sys_inst: str, google_search : bool = False) -> str:
        raise NotImplementedError("Not implemented in base class")

class GeminiBackend(LLMBackend):
    def __init__(self):
        api_key = os.getenv("GEMINI_BACKEND_API")
        if not api_key:
            raise ValueError("--- GEMINI_BACKEND_API NOT FOUND ---")

        self.client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version="v1beta"))
    print("--- GEMINI BACKEND INITIALIZED SUCCESS ---")
    
    async def generate(self, prompt_parts, temp: float, sys_inst: str, google_search : bool = False) -> str:
        print("--- GEMINI BACKEND GENERATE START ---")
        ego_config = types.GenerateContentConfig(temperature=temp, system_instruction=sys_inst)
        if google_search:
            print("--- EGO, SEARCH! ---")
            egosearch_tool = types.Tool(google_search=types.GoogleSearch())
            ego_config = types.GenerateContentConfig(temperature=temp, system_instruction=sys_inst, tools=[egosearch_tool])
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents="".join(str(prompt_parts) for part in prompt_parts) if isinstance(prompt_parts, list) else str(prompt_parts),
                config=ego_config, 
                )
            print(f"--- GEMINI BACKEND RETURN RESPONSE: {response.text} ---")
            return f"{response.text}"
        
        except Exception as e:
            print("--- GEMINI BACKEND GENERATION FAULT")
            print(f"--- EXCEPTION IS {e} ---")
            return "Excepcion"
