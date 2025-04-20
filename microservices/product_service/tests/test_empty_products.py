import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from methods import product 

class _EmptyAsyncCursor:
    def __aiter__(self): return self
    async def __anext__(self): raise StopAsyncIteration

@pytest.mark.asyncio
async def test_get_products_empty(monkeypatch):
    class FakeColl:
        def find(self): return _EmptyAsyncCursor()

    monkeypatch.setattr(product, "products_collection", FakeColl())
    monkeypatch.setattr(product, "get_inventory_stub", lambda: None)

    products = await product.get_products_with_stock()
    assert products == []
