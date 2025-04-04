from config.database import products_collection
from models.product import Product
from bson import ObjectId
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

async def get_products() -> List[dict]:
    try:
        products = []
        cursor = products_collection.find()
        async for document in cursor:
            logger.info(f"Raw MongoDB document: {document}")
            # Convert ObjectId to int if it exists
            if "_id" in document:
                document["_id"] = int(document["_id"])
            products.append(document)
        logger.info(f"Retrieved {len(products)} products from database")
        return products
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}", exc_info=True)
        raise
