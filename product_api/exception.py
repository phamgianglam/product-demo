from typing import Optional
from starlette.exceptions import HTTPException


class ItemDoesntExist(HTTPException):
    def __init__(self, detail: Optional[str] = None):
        status_code = 404
        if detail is None:
            detail = "Not Found"
        super().__init__(status_code, detail)


class ItemAlreadyExist(HTTPException):
    def __init__(self, detail: Optional[str] = None):
        status_code = 409
        if detail is None:
            detail = "Duplicated"
        super().__init__(status_code, detail)
