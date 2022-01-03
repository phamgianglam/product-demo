from datetime import datetime
import pytest
import json
from asyncio import current_task
from sqlalchemy import future
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import close_all_sessions, sessionmaker

from product_api.config import config
from product_api.model.models import BaseModel, Product


@pytest.fixture
async def async_engine():
    print(config.ASYNC_DATABASE_URL)
    async_engine = create_async_engine(
        config.ASYNC_DATABASE_URL, future=True, pool_pre_ping=True,)

    yield async_engine
    await async_engine.dispose()


@pytest.fixture
def engine():
    engine = create_engine(config.DATABASE_URL)
    yield engine
    engine.dispose()


@pytest.fixture
def reset_database(engine):
    close_all_sessions()
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)


@pytest.fixture
async def session(reset_database, async_engine):
    async_session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        future=True,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    Session = async_scoped_session(
        async_session_factory, scopefunc=current_task
    )
    async with Session() as session:
        yield session


@pytest.fixture
async def load_data(session):
    with open("tests/data.json") as f:
        data = json.load(f)

        for item in data:
            item["date"] = datetime.fromisoformat(item["date"])
            new_product = Product(**item)
            session.add(new_product)
        await session.commit()
