from fastapi import FastAPI
from starlette.exceptions import HTTPException
from product_api.config import config
from product_api.apis import config_route
from product_api.exception_handler import handle_invalid_exception, handle_normal_exception

app = FastAPI(docs_url=f"/{config.API_PREFIX}/", title="Product")

config_route(app, prefix=config.API_PREFIX)

app.add_exception_handler(HTTPException, handle_normal_exception)
app.add_exception_handler(ValueError, handle_invalid_exception)


@app.get("/healthcheck", status_code=200, include_in_schema=False)
async def healthcheck():
    return "ok"
