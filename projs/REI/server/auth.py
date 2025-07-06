import secrets
from fastapi import HTTPException, Depends, status, security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import get_db
from . import models

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def generate_api_key() -> str:
    return secrets.token_hex(32)

async def get_current_user(api_key: str = security(api_key_header), db: AsyncSession = Depends(get_db)) -> models.User:
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is missing",
        )
        
    result = await db.execute(select(models.User).where(models.User.api_key == api_key))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
    
    return user
