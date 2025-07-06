from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./EGO.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    bind=engine,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session