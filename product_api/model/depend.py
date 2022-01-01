from .config import async_session_factory
from asyncio import current_task
from sqlalchemy.ext.asyncio import async_scoped_session


async def create_session():
    from .config import async_session_factory

    Session = async_scoped_session(
        async_session_factory, scopefunc=current_task
    )
    async with Session() as session:
        yield session
