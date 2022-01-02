from datetime import datetime
from starlette.exceptions import HTTPException
from typing import List
from httpx import AsyncClient
from.config import config
client = AsyncClient()


async def update_filter_record(filter: List[str], sort: str, price: str):
    data = {"search": filter, "sort": sort,
            "price": price, "date": datetime.now().isoformat()}
    print(data)
    result = await client.post(f"{config.FILTER_RECORD_API}/filter/", json=data)
    if result.status_code != 201:
        raise HTTPException(result.status_code, result.json())
