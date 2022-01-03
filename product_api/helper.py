from typing import List
from datetime import datetime

from starlette.exceptions import HTTPException
from httpx import AsyncClient

from .config import config

client = AsyncClient()

MIN_PRICE = 0
MAX_PRICE = 1000


async def update_filter_record(filter: List[str], sort: str, price: str):
    if price is None:
        price = f"{MIN_PRICE}-{MAX_PRICE}"
    data = {
        "search": filter,
        "sort": sort,
        "price": price,
        "date": datetime.now().isoformat(),
    }
    result = await client.post(
        f"{config.FILTER_RECORD_API}/filter/", json=data
    )

    if result.status_code in range(400, 599):
        raise HTTPException(result.status_code, result.json())
