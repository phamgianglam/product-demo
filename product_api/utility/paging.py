from pydantic import BaseModel
from fastapi import Query

from sqlalchemy.future import select
from sqlalchemy.sql import Select
from sqlalchemy.sql.functions import func


DEFAULT_PAGE = 1
DEFAULT_SIZE = 100


class PagingParam(BaseModel):

    page = Query(DEFAULT_PAGE, description="requested page")
    size = Query(DEFAULT_SIZE, description="Number of collection per page")


async def paging_query(stmt: Select, page: int, size: int):
    stmt = stmt.limit(size).offset((page - 1) * size)
    return stmt


async def count_query(stmt: Select):

    sub_stmt = stmt.subquery()
    stmt = select(func.count()).select_from(sub_stmt)
    return stmt
