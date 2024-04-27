from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import async_session


async def get_session() -> AsyncGenerator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
