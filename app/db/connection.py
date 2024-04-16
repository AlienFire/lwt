from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator

# TODO получать из settings
DSN = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
engine = create_async_engine(
    DSN,
    echo=True,
)
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


# DSN

# egine and sessionmaker
