# api-gateway/models/product.py
from typing import List
from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    image: str
    slug: str

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    description: str
    category: Category
    images: List[str]

class ProductsResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    limit: int
