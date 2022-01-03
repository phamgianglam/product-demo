from datetime import datetime
import pytest
import json
from asyncio import current_task
from fastapi.testclient import TestClient
from sqlalchemy import future
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session

from sqlalchemy.orm.session import close_all_sessions, sessionmaker

from product_api.config import config
from product_api.model.models import BaseModel, Product


@pytest.fixture
async def async_engine():
    async_engine = create_async_engine(
        config.ASYNC_DATABASE_URL,
        future=True,
        pool_pre_ping=True,
    )
    yield async_engine
    await async_engine.dispose()



@pytest.fixture
def engine():

    engine = create_engine(url=config.DATABASE_URL)
    yield engine
    engine.dispose()



@pytest.fixture
def reset_database(engine):
    close_all_sessions()
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)


@pytest.fixture
async def async_session(reset_database, async_engine):
    
    async_session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        future=True,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    Session = async_scoped_session(async_session_factory, scopefunc=current_task)
    async with Session() as session_:
        yield session_



@pytest.fixture
async def load_data(async_session):
    with open("tests/data.json") as f:
        data = json.load(f)

        for item in data:
            item["date"] = datetime.fromisoformat(item["date"])
            new_product = Product(**item)
            async_session.add(new_product)
        await async_session.commit()


def create_session_override(
    session: AsyncSession,
) :
    async def create_session_():
        session.__verify_override__ = True  # type: ignore
        yield session

    return create_session_

@pytest.fixture
def app(reset_database: None):
    from product_api.app import app as _app

    yield _app


@pytest.fixture
def client(app, async_session: AsyncSession):
    from product_api.model.depend import create_session

    with TestClient(app, raise_server_exceptions=True) as client_:
        app.dependency_overrides[create_session] = create_session_override(async_session)
        yield client_

