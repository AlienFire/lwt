from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

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

