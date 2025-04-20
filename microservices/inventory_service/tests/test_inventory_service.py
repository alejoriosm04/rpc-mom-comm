import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from inventory_service.config.grpc import InventoryServiceServicer
from inventory_service.pb import inventory_pb2


@pytest.mark.asyncio
async def test_check_inventory_ok(monkeypatch):
    async def fake_check_inventory(product_id, quantity=None):
        return {"available": True, "stock": 100}

    monkeypatch.setattr(
        "inventory_service.config.grpc.check_inventory",
        fake_check_inventory
    )

    servicer = InventoryServiceServicer()

    request = inventory_pb2.InventoryRequest(product_id=1)

    class FakeContext:
        def set_code(self, code): pass
        def set_details(self, details): pass

    context = FakeContext()

    response = await servicer.CheckInventory(request, context)

    assert response.stock == 100
    assert response.available is True
