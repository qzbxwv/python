from typing import List, Dict, Any, cast
from .tools import Tool
from .llm_backend import LLMBackend
from .prompts import SEQUENTIAL_THINKING_PROMPT_RU, FINAL_SYNTHESIS_PROMPT_RU
import json5

class EGO:
    def __init__(self, backend: LLMBackend, tools: List[Tool], max_thoughts: int = 15, max_retries: int = 3):
        self.backend = backend
        self.tools: Dict[str, Tool] = {tool.name: tool for tool in tools}
        self.max_thoughts = max_thoughts
        self.max_retries = max_retries

    def _extract_json_from_response(self, text: str) -> str:
        text = text.strip()
        if '```json' in text:
            text = text.split('```json', 1)[1]
        if '```' in text:
            text = text.split('```', 1)[0]
        return text.strip()

    async def _run_ego_thinking(self, prompt_parts: str, sys_inst: str):
        thoughts_history: List[Dict[str, Any]] = []
        
        for _ in range(self.max_thoughts):
            context = {"user_query": prompt_parts, "thoughts_history": thoughts_history}
            prompt = json5.dumps(context, ensure_ascii=False)
            
            parsed_thought: Dict[str, Any] | None = None
            current_sys_inst = sys_inst

            for attempt in range(self.max_retries):
                response_text = await self.backend.generate(prompt_parts=prompt, temp=0.7, sys_inst=current_sys_inst)
                clean_json_str = self._extract_json_from_response(response_text)
                
                try:
                    parsed_json = json5.loads(clean_json_str)
                    if isinstance(parsed_json, dict):
                        parsed_thought = cast(Dict[str, Any], parsed_json)
                        break 
                except Exception as e:
                    print(f"--- JSON PARSE ERROR (Attempt {attempt + 1}/{self.max_retries}): {e} ---")
                    current_sys_inst += f"\n[СИСТЕМНАЯ ОШИБКА]: Твой JSON не парсится. Ошибка: {e}. Исправь и верни только валидный JSON."
            
            if parsed_thought is None:
                print("--- EGO FAILED TO GENERATE VALID JSON. ABORTING. ---")
                break

            thoughts_history.append({"type": "thought", "content": parsed_thought})

            tool_name = parsed_thought.get("tool_name")
            if isinstance(tool_name, str) and tool_name and tool_name.lower() != "none":
                print(f"--- EGO WANTS TO USE: {tool_name} ---")
                if tool_name in self.tools:
                    tool_to_use = self.tools[tool_name]
                    query = str(parsed_thought.get("tool_query", ""))
                    
                    try:
                        result = await tool_to_use.use(query=query, backend=self.backend)
                        thoughts_history.append({"type": "tool_output", "tool_name": tool_name, "output": result})
                    except Exception as e:
                        print(f"--- TOOL '{tool_name}' FAILED: {e} ---")
                        thoughts_history.append({"type": "tool_error", "tool_name": tool_name, "error": str(e)})
                else:
                    print(f"--- TOOL NOT FOUND: {tool_name} ---")
                    thoughts_history.append({"type": "system_note", "note": f"Инструмент '{tool_name}' не найден."})

            if parsed_thought.get("nextThoughtNeeded") is False:
               print("--- EGO DECIDED TO STOP ---")
               break
        
        return thoughts_history
    
    async def _run_egosynth(self, prompt_parts, thoughts_history, sys_inst):
        try:
            formatted_history = json5.dumps(thoughts_history, ensure_ascii=False, indent=2)
            final_prompt = sys_inst.format(user_query=prompt_parts, thoughts_history=formatted_history)
            response = await self.backend.generate(prompt_parts="", temp=0.8, sys_inst=final_prompt)
            return response
        except Exception as e:
            print(f"--- ERROR WITH EGOSYNTH: {e} ---")
            return "Синтез ответа не удался из-за внутренней ошибки."

    async def run(self, prompt_parts: str):
        print("--- RUN START ---")
        print("--- EGO THINKING START ///---")
        thoughts = await self._run_ego_thinking(prompt_parts, sys_inst=SEQUENTIAL_THINKING_PROMPT_RU)
        print("---/// EGO THINKING END ---")
        print("--- STARTING EGOSYNTH ///---")
        response = await self._run_egosynth(prompt_parts, thoughts, sys_inst=FINAL_SYNTHESIS_PROMPT_RU)
        print("---/// EGOSYNTH END ---")
        return response