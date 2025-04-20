import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from methods import product  

@pytest.mark.asyncio
async def test_get_products_inventory_failure(monkeypatch):
    async def fake_find():
        for doc in [{
            "_id": 2,
            "title": "Broken Inventory",
            "price": 10.0,
            "description": "Fail test",
            "category": {"id": 2, "name": "Broken", "image": "", "slug": ""},
            "images": []
        }]:
            yield doc

    class FakeCollection:
        def find(self):
            return fake_find()

    class BrokenStub:
        async def CheckInventory(self, request):
            raise Exception("Inventory service down")

    monkeypatch.setattr(product, "products_collection", FakeCollection())
    monkeypatch.setattr(product, "get_inventory_stub", lambda: BrokenStub())

    products = await product.get_products_with_stock()
    assert products[0]["stock"] == 0
