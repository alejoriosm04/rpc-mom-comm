# api-gateway/methods/inventory.py
import logging
from config.grpc import get_inventory_stub
from pb import inventory_pb2
from grpc import StatusCode
from methods.queue import enqueue_inventory_request

logger = logging.getLogger(__name__)

async def check_inventory_grpc(product_id: int, client_id: str = None):
    try:
        stub = get_inventory_stub()
        request = inventory_pb2.InventoryRequest(product_id=product_id)
        response = await stub.CheckInventory(request)
        logger.info(f"Inventory for product {product_id}: Available={response.available}, Stock={response.stock}")
        return {
            "product_id": product_id,
            "available": response.available,
            "stock": response.stock
        }
    except Exception as e:
        logger.error(f"Error while checking inventory: {e}")
        await enqueue_inventory_request({
            "operation": "check_inventory",
            "product_id": product_id,
            "client_id": client_id
        })
        return {
            "product_id": product_id,
            "available": False,
            "stock": 0
        }
