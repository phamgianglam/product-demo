from uuid import UUID
from typing import List, Optional, Union

from sqlalchemy.exc import IntegrityError, NoResultFound

from fastapi import APIRouter, Depends
from fastapi import Response, Request
from fastapi.param_functions import Query
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..model.depend import create_session
from ..schemas import ProductModel, ProductPostModel
from ..controller import product as ctrl
from ..model.models import Product
from ..utility.searcher import SearcherParams
from ..utility.paging import PagingParam
from ..exception import ItemAlreadyExist, ItemDoesntExist


router = APIRouter()
PREFIX = "product"


@router.post("/", response_model=ProductModel, status_code=201)
async def create_product(
    product: ProductPostModel, session: AsyncSession = Depends(create_session)
) -> Product:
    """Product API post method

    Args:
        product (ProductPostModel): product post schema
        session (AsyncSession, optional): database session. Defaults to Depends(create_session).

    Raises:
        ItemAlreadyExist: product already exist

    Returns:
        Product: Product orm object
    """
    try:
        result = await ctrl.create_resource(product, session)
    except IntegrityError:
        raise ItemAlreadyExist("product already existed")
    return result


@router.get("/", response_model=List[ProductModel], status_code=200)
async def list_all_product(
    response: Response,
    search_params=Depends(SearcherParams),
    price: Optional[Union[str,int]] = Query(
        None, description="price filter range. example: min-max"
    ),
    paging_params: PagingParam = Depends(PagingParam),
    session: AsyncSession = Depends(create_session),
) -> List[Product]:
    """API get method. List all product data satisfying on filter.If a list of
        product is successfully fetch, a request would be made to filter record
        endpoint to record user's filter. 

    Args:
        response (Response): Response obj to update header
        search_params ([type], optional): Searcher params. Defaults to Depends(SearcherParams).
        price (Optional[str], optional): Price filter. Defaults to Query( None, description="price filter range. example: min-max" ).
        paging_params (PagingParam, optional): Paging Params. Defaults to Depends(PagingParam).
        session (AsyncSession, optional): database session. Defaults to Depends(create_session).

    Raises:
        ItemDoesntExist: raise when page not found

    Returns:
        List[Product]: List of product
    """
    result, count = await ctrl.list_resource(
        price, search_params, paging_params, session
    )
    if len(result) == 0 and paging_params.page > 1:
        raise ItemDoesntExist("requestd page unavailable")

    response.headers["X-total"] = str(count)
    response.headers["X-page"] = str(paging_params.page)
    return result


@router.get("/{id}", response_model=ProductModel, status_code=200)
async def get_product(id: UUID, session=Depends(create_session)) -> Product:
    """API method to get an product by uuid
    Args:
        id (UUID): requested id
        session ([type], optional): database session. Defaults to Depends(create_session).

    Raises:
        ItemDoesntExist: [description]

    Returns:
        Product: [description]
    """
    try:
        result = await ctrl.get_resource(id, session)
    except NoResultFound:
        raise ItemDoesntExist("Product is not exist")
    return result
