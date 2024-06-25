from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from crud_fastapi.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Create a local session class using the async engine
local_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
