from config.database import orders_collection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def save_order(product_id: int, quantity: int, client_id: str):
    order_data = {
        "product_id": product_id,
        "quantity": quantity,
        "client_id": client_id,
        "status": "created",
        "created_at": datetime.utcnow()
    }

    try:
        result = await orders_collection.insert_one(order_data)
        if result.inserted_id:
            logger.info(f"Order saved successfully: product_id={product_id}, quantity={quantity}, client_id={client_id}")
            return True
        else:
            logger.error(f"Order insertion returned no ID: product_id={product_id}, quantity={quantity}, client_id={client_id}")
            return False
    except Exception as e:
        logger.error(f"Error saving order: product_id={product_id}, quantity={quantity}, client_id={client_id}, error={e}")
        return False
