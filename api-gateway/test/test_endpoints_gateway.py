# test/test_endpoints_gateway.py

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from starlette.testclient import TestClient
from app import app
from routes import order as order_route_module
from routes import product as product_route_module
from routes import inventory as inventory_route_module

client = TestClient(app)
API_KEY = os.getenv("API_KEY", "test-key")


@pytest.mark.asyncio
async def test_create_order_success(monkeypatch):
    async def mock_create_order_grpc(product_id, quantity, client_id):
        return {
            "success": True,
            "message": "Order created successfully.",
            "status": "confirmed"
        }

    monkeypatch.setattr(order_route_module, "create_order_grpc", mock_create_order_grpc)

    response = client.post(
        "/api/orders/",
        json={"product_id": 1, "quantity": 2, "client_id": "abc123"},
        headers={"x-api-key": API_KEY}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"


@pytest.mark.asyncio
async def test_create_order_fallback_rabbitmq(monkeypatch):
    async def mock_create_order_grpc(product_id, quantity, client_id):
        return {
            "success": True,
            "message": "Order service is currently unavailable. Request has been queued.",
            "status": "pending"
        }

    monkeypatch.setattr(order_route_module, "create_order_grpc", mock_create_order_grpc)

    response = client.post(
        "/api/orders/",
        json={"product_id": 1, "quantity": 2, "client_id": "abc123"},
        headers={"x-api-key": API_KEY}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    assert response.json()["message"] == "Order service is currently unavailable. Request has been queued."


@pytest.mark.asyncio
async def test_get_products_success(monkeypatch):
    async def mock_get_products_grpc(client_id=None):
        return [{
            "id": 1,
            "title": "Product 1",
            "price": 10.0,
            "description": "Sample product",
            "stock": 5,
            "category": {
                "id": 1,
                "name": "Category",
                "image": "http://image.com",
                "slug": "category"
            },
            "images": ["http://image.com/img1.png"]
        }]

    monkeypatch.setattr(product_route_module, "get_products_grpc", mock_get_products_grpc)

    response = client.get("/api/products/?page=1&limit=12", headers={"x-api-key": API_KEY})

    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert data["total"] == 1


@pytest.mark.asyncio
async def test_check_inventory_success(monkeypatch):
    async def mock_check_inventory_grpc(product_id, client_id=None):
        return {
            "product_id": product_id,
            "available": True,
            "stock": 10
        }

    monkeypatch.setattr(inventory_route_module, "check_inventory_grpc", mock_check_inventory_grpc)

    response = client.get("/api/inventory/check?product_id=1", headers={"x-api-key": API_KEY})

    assert response.status_code == 200
    data = response.json()
    assert data["available"] is True
    assert data["stock"] == 10
