from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from fastapi import Request


def handle_normal_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}
    )


def handle_invalid_exception(request: Request, exc: Exception):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
