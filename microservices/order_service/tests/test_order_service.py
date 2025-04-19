import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.grpc import OrderServiceServicer
from pb import order_pb2
import methods.order as order_methods  


class FakeContext:
    def set_code(self, code): pass
    def set_details(self, details): pass


@pytest.mark.asyncio
async def test_create_order_success(monkeypatch):
    async def fake_check_inventory(product_id, quantity): return True
    async def fake_save_order(product_id, quantity, client_id): return True
    async def fake_reduce_stock(product_id, quantity): return True

    monkeypatch.setattr(order_methods, "check_inventory", fake_check_inventory)
    monkeypatch.setattr(order_methods, "reduce_stock", fake_reduce_stock)
    monkeypatch.setattr(order_methods, "save_order", fake_save_order)

    servicer = OrderServiceServicer()
    request = order_pb2.OrderRequest(product_id=1, quantity=2, client_id="abc123")
    response = await servicer.CreateOrder(request, FakeContext())

    assert response.success is True
    assert response.message == "Order created successfully."


@pytest.mark.asyncio
async def test_create_order_no_stock(monkeypatch):
    async def fake_check_inventory(product_id, quantity): return False

    monkeypatch.setattr(order_methods, "check_inventory", fake_check_inventory)

    servicer = OrderServiceServicer()
    request = order_pb2.OrderRequest(product_id=1, quantity=5, client_id="no-stock")
    response = await servicer.CreateOrder(request, FakeContext())

    assert response.success is False
    assert "insufficient stock" in response.message.lower()


@pytest.mark.asyncio
async def test_create_order_reduce_stock_fail(monkeypatch):
    async def fake_check_inventory(product_id, quantity): return True
    async def fake_reduce_stock(product_id, quantity): return False
    async def fake_save_order(product_id, quantity, client_id): return True

    monkeypatch.setattr(order_methods, "check_inventory", fake_check_inventory)
    monkeypatch.setattr(order_methods, "reduce_stock", fake_reduce_stock)
    monkeypatch.setattr(order_methods, "save_order", fake_save_order)

    servicer = OrderServiceServicer()
    request = order_pb2.OrderRequest(product_id=1, quantity=1, client_id="reduce-fail")
    response = await servicer.CreateOrder(request, FakeContext())

    assert response.success is False
    assert "could not reduce stock" in response.message.lower()


@pytest.mark.asyncio
async def test_create_order_save_fail(monkeypatch):
    async def fake_check_inventory(product_id, quantity): return True
    async def fake_reduce_stock(product_id, quantity): return True
    async def fake_save_order(product_id, quantity, client_id): return False

    monkeypatch.setattr(order_methods, "check_inventory", fake_check_inventory)
    monkeypatch.setattr(order_methods, "reduce_stock", fake_reduce_stock)
    monkeypatch.setattr(order_methods, "save_order", fake_save_order)

    servicer = OrderServiceServicer()
    request = order_pb2.OrderRequest(product_id=1, quantity=3, client_id="save-fail")
    response = await servicer.CreateOrder(request, FakeContext())

    assert response.success is False
    assert "could not save order" in response.message.lower()


@pytest.mark.asyncio
async def test_create_order_unexpected_error(monkeypatch):
    async def fake_check_inventory(product_id, quantity): raise Exception("Unexpected error")

    monkeypatch.setattr(order_methods, "check_inventory", fake_check_inventory)

    servicer = OrderServiceServicer()
    request = order_pb2.OrderRequest(product_id=1, quantity=2, client_id="error")
    response = await servicer.CreateOrder(request, FakeContext())

    assert response.success is False
    assert "internal error" in response.message.lower()
