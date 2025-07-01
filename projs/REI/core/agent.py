from typing import List, Dict
from .tools import Tool, GoogleSearch, PythonCodeExec, WikiAPI
from .llm_backend import LLMBackend, FakeGeminiBackend

class REIAgent:
    def __init__(self, backend : LLMBackend, tools : List[Tool]):
        self.backend = backend
        self.tools : Dict[str, Tool] = {tool.name: tool for tool in tools}
    
    def run(self, prompt_parts):
        pass
    
    def _run_sequential_thinking(self, seq_prompt, prompt_parts):
        pass
        