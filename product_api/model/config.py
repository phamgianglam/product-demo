from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from ..config import config


engine = create_async_engine(
    config.ASYNC_DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)
async_session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
    class_=AsyncSession,
    expire_on_commit=False,
)
