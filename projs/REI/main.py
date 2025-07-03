from core.agent import EGO
from core.tools import Tool, EgoSearch, PythonCodeExec, WikiAPI
from core.llm_backend import LLMBackend, GeminiBackend
import asyncio


async def main():
    print("--- Configuring EGO---")

    print("--- BACKEND ---")
    backend_instanse = GeminiBackend()
    print("--- BACKEND READY ---")

    print("--- TOOLS ---")
    tools_list = [EgoSearch(), PythonCodeExec(), WikiAPI()]
    print("--- TOOLS READY ---")

    print("--- EGO Emergent. Grasp. ---")
    ego_instanse = EGO(backend=backend_instanse, tools=tools_list)
    print("--- Organism ---")

    print("--- EGO INFO ---")
    print(f"BACKEND : {type(ego_instanse.backend)}")
    print(f"TOOLS : {list(ego_instanse.tools.keys())}")

    first_tool_name = list(ego_instanse.tools.keys())[0]
    print(f"FIRST TOOL'{first_tool_name}':")
    print(f"  - NAME: {ego_instanse.tools[first_tool_name].name}")
    print(f"  - DESCRIPTION: {ego_instanse.tools[first_tool_name].desc}")

    print("--- BACKEND START ---")
    response = await ego_instanse.run(str(input("Get EGO a work: ")))
    print("--- BACKEND  END ---")


if __name__ == "__main__":
    asyncio.run(main())

