import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from inventory_service.config.grpc import InventoryServiceServicer
from inventory_service.pb import inventory_pb2

@pytest.mark.asyncio
async def test_reduce_stock_ok(monkeypatch):
    async def fake_reduce_stock(product_id, quantity):
        return True

    monkeypatch.setattr(
        "inventory_service.config.grpc.reduce_stock",
        fake_reduce_stock
    )

    servicer = InventoryServiceServicer()

    request = inventory_pb2.InventoryUpdateRequest(
        product_id=1,
        quantity=5
    )

    class FakeContext:
        def set_code(self, code): pass
        def set_details(self, details): pass

    context = FakeContext()
    response = await servicer.ReduceStock(request, context)

    assert response.success is True
