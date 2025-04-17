from pydantic import BaseModel
from datetime import datetime

class InventoryItem(BaseModel):
    product_id: int
    stock: int
    available: bool
    updated_at: datetime
