from os import error
from re import search
from uuid import UUID
from fastapi import APIRouter, Depends, exceptions, HTTPException
from fastapi import Response
from typing import List, Optional

from fastapi.param_functions import Query
from sqlalchemy.sql.operators import op

from product_api.utility.searcher import SearcherParams

from ..model.depend import create_session
from ..schemas import ProductModel, ProductPostModel
from ..controller import product as ctrl
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..utility.paging import PagingParam

router = APIRouter()
PREFIX = "product"


@router.post("/", response_model=ProductModel, status_code=201)
async def create_product(
    series: ProductPostModel, session=Depends(create_session)
):
    try:
        result = await ctrl.create_resource(series, session)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=409, detail="given product is a duplicate"
        )
    return result


@router.get("/", response_model=List[ProductModel], status_code=200)
async def list_all_product(
    response: Response,
    search_params=Depends(SearcherParams),
    price: Optional[str] = Query(
        None, description="price filter range. example: min-max"),
    paging_params=Depends(PagingParam),
    session=Depends(create_session),
):

    result, count = await ctrl.list_resource(price, search_params, paging_params, session)

    response.headers["X-total"] = str(count)
    response.headers["X-page"] = str(paging_params.page)
    return result


@router.get("/{id}", response_model=ProductModel, status_code=200)
async def get_product(id: UUID, session=Depends(create_session)):
    try:
        result = await ctrl.get_resource(id, session)
    except NoResultFound as exc:
        raise HTTPException(status_code=404, detail=f"product is not found")
    return result
