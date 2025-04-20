import sys
import os
import pytest
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from methods.product import get_products_with_stock

@pytest.mark.asyncio
@patch('methods.product.get_inventory_stub')
@patch('methods.product.products_collection.find')
async def test_get_products_with_stock(mock_find, mock_get_inventory_stub):
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = [
        {
            "_id": 1,
            "title": "Test",
            "price": 9.99,
            "description": "desc",
            "category": {"id": 1, "name": "cat", "image": "img", "slug": "cat"},
            "images": []
        }
    ]
    mock_find.return_value = mock_cursor

    mock_inventory_stub = AsyncMock()
    mock_inventory_stub.CheckInventory.return_value.stock = 5
    mock_get_inventory_stub.return_value = mock_inventory_stub

    products = await get_products_with_stock()

    assert len(products) == 1
    assert products[0]['stock'] == 5
    assert products[0]['_id'] == 1
