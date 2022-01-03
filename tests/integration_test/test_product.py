import pytest
import respx
from datetime import datetime
from fastapi.testclient import TestClient
from httpx import Response
from product_api.config import config

def test_post(client: TestClient, load_data):
    data = {"name": "example", "description": "description",
            "price": 50, "date": datetime.now().isoformat()}
    response = client.post("/api/product/", json=data)
    assert response.status_code == 201



def test_get( client: TestClient):
    data = {"search": "example", "sort": "description",
            "price": "20-20", "date": datetime.now().isoformat()}
    with respx.mock(assert_all_mocked=False):
        respx.post( f"{config.FILTER_RECORD_API}/filter", json=data).mock(return_value=Response(201))
        response = client.get("/api/product")
        assert response.status_code == 200
