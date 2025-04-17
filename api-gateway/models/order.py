# models/order.py
from pydantic import BaseModel

class OrderRequest(BaseModel):
    product_id: int
    quantity: int
    client_id: str

class OrderResponse(BaseModel):
    success: bool
    message: str
