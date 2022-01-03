from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi import Response
from typing import List, Optional

from fastapi.param_functions import Query
from product_api.exception import ItemAlreadyExist, ItemDoesntExist

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
        raise ItemAlreadyExist("product already existed")
    return result


@router.get("/", response_model=List[ProductModel], status_code=200)
async def list_all_product(
    response: Response,
    search_params=Depends(SearcherParams),
    price: Optional[str] = Query(
        None, description="price filter range. example: min-max"
    ),
    paging_params: PagingParam = Depends(PagingParam),
    session=Depends(create_session),
):

    result, count = await ctrl.list_resource(
        price, search_params, paging_params, session
    )
    if len(result) == 0 and paging_params.page > 1:
        raise ItemDoesntExist("requestd page unavailable")

    response.headers["X-total"] = str(count)
    response.headers["X-page"] = str(paging_params.page)
    return result


@router.get("/{id}", response_model=ProductModel, status_code=200)
async def get_product(id: UUID, session=Depends(create_session)):
    try:
        result = await ctrl.get_resource(id, session)
    except NoResultFound as exc:
        raise ItemDoesntExist("Product is not exist")
    return result
