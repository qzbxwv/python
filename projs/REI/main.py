from fastapi import FastAPI, Depends
from core.agent import EGO
from core.tools import EgoSearch, EgoCode, EgoWiki, AlterEgo
from core.llm_backend import GeminiBackend
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from server.database import get_db
from server import models, auth

from server import models, schemas, auth, database

app = FastAPI()
ego_instance: EGO | None = None

class EgoRequest(BaseModel):
    query: str

@app.on_event('startup')
async def startup_event():
    global ego_instance
    backend_instance = GeminiBackend()
    tools = [EgoSearch(), EgoCode(), EgoWiki(), AlterEgo()]
    ego_instance = EGO(backend=backend_instance, tools=tools)
    print('--- EGO READY TO GET OVER YOU ---')

@app.post("/users/register", response_model=schemas.UserOut)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    #TODO тут логика проверки, что юзер не существует
    api_key = auth.generate_api_key()
    new_user = models.User(username=user.username, api_key=api_key)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/ego/v1/ask")
# TODO UPDATE this endpoint to use the new EgoRequest schema AND SAVE HISTORY
async def ask_ego(request: EgoRequest):
    if ego_instance is None:
        return {"error": "EGO is not initialized."}
    response = await ego_instance.run(request.query)
    return {"response": response}

@app.delete("/ego/v1/clear_history")
async def clear_history(current_user: models.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(delete(models.RequestLog).where(models.RequestLog.user_id == current_user.id))
    await db.commit()
    return {"status": "success", "message": "History cleared for current user."}