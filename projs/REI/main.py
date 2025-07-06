from fastapi import FastAPI
from core.agent import EGO
from core.tools import Tool, EgoSearch, EgoCode, EgoWiki, AlterEgo
from core.llm_backend import LLMBackend, GeminiBackend
import asyncio
from pydantic import BaseModel

app = FastAPI()
ego = None

class EgoRequest(BaseModel):
    query : str

@app.on_event('startup')
async def startup_event():
    global ego
    backend_instance = GeminiBackend()
    tools = [EgoSearch(), EgoCode(), EgoWiki(), AlterEgo()]
    ego = EGO(backend=backend_instance, tools=tools)
    print('--- EGO READY TO GET OVER YOU ---')


@app.post("/ego/v1/ask")
async def ask_ego(request: EgoRequest):
    global ego
    if not ego:
        return {"error": "EGO is not initialized."}
    
    user_query = request.query
    response = await ego.run(user_query)
    return {"response": response}
