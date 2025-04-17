from config.database import products_collection
from config.inventory_grpc_client import get_inventory_stub
from pb import inventory_pb2
import logging

logger = logging.getLogger(__name__)

async def get_products_with_stock():
    products = []
    cursor = products_collection.find()
    inventory_stub = get_inventory_stub()

    async for doc in cursor:
        stock = 0
        try:
            response = await inventory_stub.CheckInventory(
                inventory_pb2.InventoryRequest(product_id=int(doc["_id"]))
            )
            stock = response.stock
        except Exception as e:
            logger.warning(f"Error fetching stock for product {doc['_id']}: {str(e)}")

        doc["_id"] = int(doc["_id"])
        doc["stock"] = stock

        products.append(doc) 

    return products
