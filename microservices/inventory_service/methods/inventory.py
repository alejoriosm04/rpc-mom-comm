# methods/inventory.py
from config.database import inventory_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

async def check_inventory(product_id: int) -> dict:
    try:
        result = await inventory_collection.find_one({"product_id": product_id})
        if result:
            return {
                "available": result["stock"] > 0,
                "stock": result["stock"]
            }
        return {"available": False, "stock": 0}
    except Exception as e:
        logger.error(f"Error checking inventory: {e}")
        raise
