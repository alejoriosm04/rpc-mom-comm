# models/order.py
from config.database import orders_collection
from datetime import datetime

async def save_order(product_id: int, quantity: int, client_id: str):
    order_data = {
        "product_id": product_id,
        "quantity": quantity,
        "client_id": client_id,
        "status": "created",
        "created_at": datetime.utcnow()
    }
    await orders_collection.insert_one(order_data)
