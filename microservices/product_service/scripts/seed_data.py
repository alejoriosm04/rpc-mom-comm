import asyncio
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import products_collection
from models.product import Product, Category
from datetime import datetime

async def seed_products():
    # Clear existing data
    await products_collection.delete_many({})
    
    # Sample categories
    categories = [
        Category(
            id=1,
            name="Electronics",
            image="https://img.freepik.com/free-photo/beautiful-view-sunset-sea_23-2148019892.jpg",
            slug="electronics"
        ),
        Category(
            id=2,
            name="Clothing",
            image="https://img.freepik.com/free-photo/beautiful-view-sunset-sea_23-2148019892.jpg",
            slug="clothing"
        ),
        Category(
            id=3,
            name="Books",
            image="https://img.freepik.com/free-photo/beautiful-view-sunset-sea_23-2148019892.jpg",
            slug="books"
        )
    ]

    # Sample products
    products = [
        {
            "_id": 1,
            "title": "Smartphone X",
            "price": 999.99,
            "description": "Latest smartphone with amazing features",
            "category": categories[0].model_dump(),
            "images": [
                "https://img.freepik.com/free-photo/beautiful-view-sunset-sea_23-2148019892.jpg",
            ]
        },
        {
            "_id": 2,
            "title": "Classic T-Shirt",
            "price": 29.99,
            "description": "Comfortable cotton t-shirt",
            "category": categories[1].model_dump(),
            "images": [
                "https://img.freepik.com/free-photo/beautiful-view-sunset-sea_23-2148019892.jpg",
            ]
        },
        {
            "_id": 3,
            "title": "Programming Guide",
            "price": 49.99,
            "description": "Comprehensive programming guide",
            "category": categories[2].model_dump(),
            "images": [
                "https://img.freepik.com/free-photo/beautiful-view-sunset-sea_23-2148019892.jpg",
            ]
        }
    ]

    # Insert products
    for product in products:
        await products_collection.insert_one(product)
        print(f"Inserted product: {product['title']}")

    print("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_products()) 