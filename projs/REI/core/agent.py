from typing import List, Dict
from .tools import Tool, GoogleSearch, PythonCodeExec, WikiAPI
from .llm_backend import LLMBackend, GeminiBackend
from . import prompts
import json5

class REIAgent:
    def __init__(self, backend: LLMBackend, tools: List[Tool]):
        self.backend = backend
        self.tools: Dict[str, Tool] = {tool.name: tool for tool in tools}

    async def _run_sequential_thinking(self, prompt_parts, sys_inst):
        thoughs_history = []
        nextThoughtNeeded = True

        while nextThoughtNeeded:
            prompt = f"Запрос: {prompt_parts}. История мыслей: {json5.dumps(thoughs_history)}"

            thought = await self.backend.generate(prompt_parts=prompt, temp=0.8, sys_inst=sys_inst)

            try:
                parsed_thought = json5.loads(thought)
                if not isinstance(parsed_thought, Dict):
                    print("LLM returned non-valid json")
                    nextThoughtNeeded = False
                    continue
            except Exception as e:
                print("Ошибка парсинга JSON")
                print(f"Был получен :{thought}")
                print(f"Ошибка: {e}")
                nextThoughtNeeded = False
                continue

            tool_name_from_llm = parsed_thought.get("tool_name")
            if tool_name_from_llm:
                print(f"Агент хочет использовать {tool_name_from_llm}")
                if tool_name_from_llm in self.tools:
                    tool_use = self.tools[tool_name_from_llm]
                    tool_use_query = str(parsed_thought.get("tool_query"))
                    tool_result = tool_use.use(tool_use_query)
                    print(f"Результат использования Tool: {tool_result}")
                    tool_result_thought = {
                        "type": "tool_output",
                        "tool_name": tool_name_from_llm,
                        "tool_output": str(tool_result),
                    }
                    thoughs_history.append((tool_result_thought))
                else:
                    print(
                        f"Получено неверное название инструмента {tool_name_from_llm}"
                    )

            thoughs_history.append(parsed_thought)
            # TODO добавить проверку на ответ nextThoughtNeeded модели
            nextThoughtNeeded = False
        return thoughs_history
    
    async def _run_synthesist(self, prompt_parts, thoughs_history, sys_inst):
        return prompt_parts, thoughs_history, sys_inst


    async def run(self, prompt_parts):
        
        thoughts = await self._run_sequential_thinking(prompt_parts, sys_inst=prompts.SEQUENTIAL_THINKING_PROMPT_RU)

        response = await self._run_synthesist(prompt_parts, thoughts, sys_inst=prompts.FINAL_SYNTHESIS_PROMPT_RU)

        return response


