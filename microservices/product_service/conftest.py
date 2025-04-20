import pytest
from unittest.mock import AsyncMock

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
def stub_inventory_ok():
    stub = AsyncMock()
    stub.CheckInventory.return_value.stock = 99
    return stub
