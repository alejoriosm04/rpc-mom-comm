import pytest
import asynctest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from product_service.methods import product

@pytest.mark.asyncio
async def test_get_products_empty(monkeypatch):
    async def fake_find():
        return
        yield  

    class AsyncEmptyCursor:
        def __aiter__(self):
            return self

        async def __anext__(self):
            raise StopAsyncIteration

    class FakeCollection:
        def find(self):
            return AsyncEmptyCursor()

    monkeypatch.setattr(product, "products_collection", FakeCollection())
    monkeypatch.setattr(product, "get_inventory_stub", lambda: None) 

    products = await product.get_products_with_stock()
    assert products == []