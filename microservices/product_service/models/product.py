from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class Category(BaseModel):
    id: int
    name: str
    image: str
    slug: str

class Product(BaseModel):
    id: int = Field(alias="_id")
    title: str
    price: float
    description: str
    category: Category
    images: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }

