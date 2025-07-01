from core.agent import REIAgent
from core.tools import Tool, GoogleSearch, PythonCodeExec, WikiAPI
from core.llm_backend import LLMBackend, FakeGeminiBackend

def main():
    print("--- Configuring REI ---")
    
    print("--- BACKEND/// ---")
    backend_instanse = FakeGeminiBackend(api_key="SOMEAPIKEY")
    print("--- ///BACKEND READY ---")
    
    print("--- TOOLS GETTING READY/// ---")
    tools_list = [GoogleSearch(), PythonCodeExec(), WikiAPI()]
    print("--- ///TOOLS READY ---")
    
    print("--- REI Reflect. Evaluate.///")
    rei_instanse = REIAgent(backend=backend_instanse, tools=tools_list)
    print("--- ///INTELLIGENSE ---")
    
    print("--- REI INFO ---")
    print(f"BACKEND : {type(rei_instanse.backend)}")
    print(f"TOOLS : {list(rei_instanse.tools.keys())}")
    
    
    first_tool_name = list(rei_instanse.tools.keys())[0]
    print(f"FIRST TOOL'{first_tool_name}':")
    print(f"  - NAME: {rei_instanse.tools[first_tool_name].name}")
    print(f"  - DESCRIPTION: {rei_instanse.tools[first_tool_name].desc}")
    
    
if __name__ == "__main__":
    main()