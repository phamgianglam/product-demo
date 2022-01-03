from re import search
import pytest
import respx
from datetime import datetime
from fastapi.testclient import TestClient
from httpx import Response
from product_api.config import config


def test_post(client: TestClient, load_data):
    data = {
        "name": "example",
        "description": "description",
        "price": 50,
        "date": datetime.now().isoformat(),
    }
    response = client.post("/api/product/", json=data)
    assert response.status_code == 201


@pytest.mark.parametrize(
    "search, order, price",
    [("sample", None, None), ("sample", "price:asc", "20-100")],
)
def test_get_product_with_various_params(
    respx_mock, search, order, price, client: TestClient, load_data
):
    data = {
        "search": "example",
        "sort": "description",
        "price": "20-20",
        "date": datetime.now().isoformat(),
    }
    print(f"{config.FILTER_RECORD_API}/filter")
    with respx.mock(assert_all_mocked=False):

        respx.post(f"{config.FILTER_RECORD_API}/filter", json=data).mock(
            return_value=Response(201)
        )
        response = client.get(
            "/api/product",
            params={"search": search, "order": order, "price": price},
        )
        print(response.json())
        assert response.status_code == 200


def test_get_no_page_found(client: TestClient):
    data = {
        "search": "example",
        "sort": "description",
        "price": "20-20",
        "date": datetime.now().isoformat(),
    }

    with respx.mock(assert_all_mocked=False):

        respx.post(f"{config.FILTER_RECORD_API}/filter", json=data).mock(
            return_value=Response(201)
        )
        response = client.get("/api/product", params={"page": 2, "size": 100})
        assert response.status_code == 404
