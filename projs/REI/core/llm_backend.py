class LLMBackend:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def generate(self, prompt_parts, temp : float, top_p : float, top_k : float, sys_inst : str) -> str:
        raise NotImplementedError("Not implemented in base class")

class FakeGeminiBackend(LLMBackend):
    def __init__(self, api_key):
        super().__init__(api_key)
        
    def generate(self, prompt_parts, temp: float, top_p: float, top_k: float, sys_inst: str) -> str:
        print("Fake Gemini backend Вызван")
        return "Это фейковый ответ от Gemini"