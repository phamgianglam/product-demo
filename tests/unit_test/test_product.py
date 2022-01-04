import pytest
from datetime import datetime
from unittest.mock import patch
from uuid import uuid4

from sqlalchemy.exc import IntegrityError, NoResultFound

from product_api.schemas import ProductPostModel
from product_api.controller import product as ctrl
from product_api.utility.paging import PagingParam
from product_api.utility.searcher import SearcherParams

pytestmark = pytest.mark.asyncio


async def test_create_product(async_session):
    product = ProductPostModel(
        name="example",
        description="description",
        price=50,
        date=datetime.now(),
    )

    result = await ctrl.create_resource(product, async_session)
    assert result.name == product.name


async def test_create_product_duplicate(async_session):
    product = ProductPostModel(
        name="example",
        description="description",
        price=50,
        date=datetime.now(),
    )

    result = await ctrl.create_resource(product, async_session)
    assert result.name == product.name
    with pytest.raises(IntegrityError):
        await ctrl.create_resource(product, async_session)


async def test_get_product(async_session):
    product = ProductPostModel(
        name="example",
        description="description",
        price=50,
        date=datetime.now(),
    )

    result = await ctrl.create_resource(product, async_session)
    assert result.name == product.name

    result = await ctrl.get_resource(result.id_, async_session)
    assert result.name == product.name


async def test_get_product_not_found(async_session):
    with pytest.raises(NoResultFound):
        await ctrl.get_resource(uuid4(), async_session)


@patch("product_api.controller.product.update_filter_record")
async def test_get_all_data(mock_update_record, async_session, load_data):
    search = SearcherParams(search=None, order=None, df=None)
    paging_param = PagingParam()
    mock_update_record.return_value = None
    result, count = await ctrl.list_resource(
        None, search, paging_param, async_session
    )
    assert count == 4


@pytest.mark.parametrize(
    "price, result_count", [("100-150", 2), ("100-800", 3)]
)
@patch("product_api.controller.product.update_filter_record")
async def test_get_all_data_filter_by_price(
    mock_update_record, price, result_count, async_session, load_data
):
    search = SearcherParams(search=None, order=None, df=None)
    paging_param = PagingParam()
    mock_update_record.return_value = None
    result, count = await ctrl.list_resource(
        price, search, paging_param, async_session
    )
    assert count == result_count


@pytest.mark.parametrize(
    "search, result_count", [("name:sample", 3), ("description:vpn", 1)]
)
@patch("product_api.controller.product.update_filter_record")
async def test_get_all_data_filter_by_search(
    mock_update_record, search, result_count, async_session, load_data
):
    search = SearcherParams(search=search, order=None, df=None)
    paging_param = PagingParam()
    mock_update_record.return_value = None
    result, count = await ctrl.list_resource(
        None, search, paging_param, async_session
    )
    assert count == result_count


@patch("product_api.controller.product.update_filter_record")
async def test_get_all_data_no_found(mock_update_record, async_session, load_data):
    search = SearcherParams(search=None, order=None, df=None)
    paging_param = PagingParam(page=2, size=100)
    mock_update_record.return_value = None
    result, count = await ctrl.list_resource(
        None, search, paging_param, async_session
    )
    assert result == []
