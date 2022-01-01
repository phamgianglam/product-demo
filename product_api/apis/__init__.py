from fastapi import FastAPI
from . import product


def config_route(app: FastAPI, dependencies=None, prefix=None):
    app.include_router(
        product.router,
        prefix=f"/{prefix}/{product.PREFIX}",
        tags=[product.PREFIX],
    )
