from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .config import sess
from app.database.redis import RedisSession


async def create_session() -> AsyncGenerator[AsyncSession, None]:
    async with sess() as session:
        yield session


async def get_redis_db() -> RedisSession:
    async with RedisSession as session:
        yield session
