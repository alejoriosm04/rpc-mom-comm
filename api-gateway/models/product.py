# models/product.py
from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    description: str
