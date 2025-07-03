from typing import List, Dict

from google.genai.types import ReplayResponse
from .tools import Tool, EgoSearch, PythonCodeExec, WikiAPI
from .llm_backend import LLMBackend, GeminiBackend
from .prompts import SEQUENTIAL_THINKING_PROMPT_RU, FINAL_SYNTHESIS_PROMPT_RU, EGO_SEARCH_PROMPT_RU
import json5

class EGO:
    def __init__(self, backend: LLMBackend, tools: List[Tool]):
        self.backend = backend
        self.tools: Dict[str, Tool] = {tool.name: tool for tool in tools}

    async def _run_ego_thinking(self, prompt_parts, sys_inst):
        thoughs_history = []
        nextThoughtNeeded = True

        while nextThoughtNeeded:
            prompt = f"Запрос: {prompt_parts}. История мыслей: {json5.dumps(thoughs_history)}"

            thought = await self.backend.generate(prompt_parts=prompt, temp=0.8, sys_inst=sys_inst)
            
            clean_thought = thought.strip()

            if clean_thought.startswith("```json"):
                clean_thought = clean_thought[7:]
            
            if clean_thought.startswith("```"):
                clean_thought = clean_thought[3:]

            if clean_thought.endswith('```'):
                clean_thought = clean_thought[:-3]

            try:
                parsed_thought = json5.loads(clean_thought)
                if not isinstance(parsed_thought, Dict):
                    print("LLM RETURNED NOT-VALID JSON")
                    nextThoughtNeeded = False
                    continue
            except Exception as e:
                print("--- JSON PARSE ERROR ---")
                print(f"--- JSON:{thought} ---")
                print(f"--- ERROR: {e} ---")
                nextThoughtNeeded = False
                continue

            tool_name_from_llm = parsed_thought.get("tool_name")
            if tool_name_from_llm == "EgoSearch":
                print("--- EGO WANTS TO USE EGOSEARCH ---")
                egosearch_query = str(parsed_thought.get("tool_query"))
                print('--- EGO QUERY: ', egosearch_query)
                egosearch_result = await self.backend.generate(prompt_parts=egosearch_query, temp=0.9, sys_inst=EGO_SEARCH_PROMPT_RU, google_search=True)
                thoughs_history.append(egosearch_result)
            elif tool_name_from_llm != "EgoSearch":
                print(f"--- EGO WANTS TO USE {tool_name_from_llm} ---")
                if tool_name_from_llm in self.tools:
                    tool_use = self.tools[tool_name_from_llm]
                    tool_use_query = str(parsed_thought.get("tool_query"))
                    tool_result = await tool_use.use(tool_use_query)
                    print(f"--- TOOL USED WITH RESULT: {tool_result} ---")
                    tool_result_thought = {
                        "type": "tool_output",
                        "tool_name": tool_name_from_llm,
                        "tool_output": str(tool_result),
                    }
                    thoughs_history.append((tool_result_thought))
                else:
                    print(
                        f"--- TOOL NOT FOUND: {tool_name_from_llm} ---"
                    )

            thoughs_history.append(parsed_thought)
            
            next_thoughts = parsed_thought.get("nextThoughtNeeded")
            if next_thoughts:
                continue
            else:
                nextThoughtNeeded = False
                print("--- NEXT THOUGHTS FALSE ---")
            nextThoughtNeeded = False

        return thoughs_history
    
    async def _run_egosynth(self, prompt_parts, thoughs_history, sys_inst):
        prompt = f"Запрос: {prompt_parts}. Мысли для синтеза: {thoughs_history}"

        try:
            response = await self.backend.generate(prompt_parts=prompt, temp=0.9, sys_inst=sys_inst)
            return response
        except Exception as e:
            print("--- ERROR WITH BACKEND ---")
            print(f"--- ERROR IS {e} ---")  


    async def run(self, prompt_parts):
        print("--- RUN START ---")
        print("--- EGO THINKING START ///---")
        thoughts = await self._run_ego_thinking(prompt_parts, sys_inst=SEQUENTIAL_THINKING_PROMPT_RU)
        print("---/// EGO THINKING END ---")
        print("--- STARTING EGOSYNTH ///---")
        response = await self._run_egosynth(prompt_parts, thoughts, sys_inst=FINAL_SYNTHESIS_PROMPT_RU)
        print("---/// EGOSYNTH END ---")

        return response


