import json5
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
from typing import List, Optional

load_dotenv()

class LLMBackend:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, prompt_parts: str, temp: float, sys_inst: str, tools: Optional[List[types.Tool]] = None) -> str:
        raise NotImplementedError("Not implemented in base class")

class GeminiBackend(LLMBackend):
    def __init__(self):
        api_key = os.getenv("GEMINI_BACKEND_API")
        if not api_key:
            raise ValueError("--- GEMINI_BACKEND_API NOT FOUND ---")
        
        # Инициализируем через Client, как ты и хотел.
        self.client = genai.Client(api_key=api_key)
        print("--- GEMINI BACKEND INITIALIZED SUCCESS ---")
    
    async def generate(self, prompt_parts: str, temp: float, sys_inst: str, tools: Optional[List[types.Tool]] = None) -> str:
        print("--- GEMINI BACKEND GENERATE START ---")
        
        # Создаем конфигурацию. System instruction передается здесь.
        config = types.GenerateContentConfig(
            temperature=temp,
            system_instruction=sys_inst
        )
        
        generation_kwargs = {
            "model": 'gemini-2.5-flash-lite-preview-06-17',
            "contents": prompt_parts,
            "config": config,
        }
        
        if tools:
            # Обновляем конфиг, добавляя инструменты
            config.tools = tools
            generation_kwargs["config"] = config

        try:
            # Асинхронный вызов через client.aio
            response = await self.client.aio.models.generate_content(**generation_kwargs)
            
            response_text = response.text if hasattr(response, 'text') and response.text is not None else ""
            print(f"--- GEMINI BACKEND RETURN RESPONSE: {response_text} ---")
            return response_text
            
        except Exception as e:
            print(f"--- GEMINI BACKEND GENERATION FAULT: {e} ---")
            return '{"thoughts": "Произошла ошибка при генерации ответа.", "evaluate": "Критическая ошибка бэкенда.", "confidence": 0.0, "tool_name": null, "nextThoughtNeeded": false}'