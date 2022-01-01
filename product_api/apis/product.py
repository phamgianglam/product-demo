from os import error
from uuid import UUID
from fastapi import APIRouter, Depends, exceptions, HTTPException
from fastapi import Response
from typing import List

from fastapi.param_functions import Query

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
    name=Query(None, description="name of product"),
    params=Depends(PagingParam),
    session=Depends(create_session),
):

    result, count = await ctrl.list_resource(name, params, session)

    response.headers["X-total"] = str(count)
    response.headers["X-page"] = str(params.page)
    return result


@router.get("/{id}", response_model=ProductModel, status_code=200)
async def get_product(id: UUID, session=Depends(create_session)):
    try:
        result = await ctrl.get_resource(id, session)
    except NoResultFound as exc:
        raise HTTPException(status_code=404, detail=f"product is not found")
    return result
