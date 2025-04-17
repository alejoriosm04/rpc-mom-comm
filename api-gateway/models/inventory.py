# models/inventory.py
from pydantic import BaseModel

class InventoryResponse(BaseModel):
    product_id: int
    available: bool
    stock: int
