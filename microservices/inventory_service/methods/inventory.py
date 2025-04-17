from config.database import inventory_collection
from datetime import datetime
from config.product_grpc_client import get_product_stub
from pb import product_pb2

async def check_inventory(product_id: int, quantity: int):
    item = await inventory_collection.find_one({"product_id": product_id})

    if not item or item["stock"] < quantity:
        return {"available": False, "stock": item["stock"] if item else 0}

    return {"available": True, "stock": item["stock"]}

async def reduce_stock(product_id: int, quantity: int):
    result = await inventory_collection.update_one(
        {"product_id": product_id, "stock": {"$gte": quantity}},
        {"$inc": {"stock": -quantity}, "$set": {"updated_at": datetime.utcnow()}}
    )
    return result.modified_count == 1
