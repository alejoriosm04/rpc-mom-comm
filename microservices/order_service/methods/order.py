from pb import order_pb2, order_pb2_grpc
from config.inventory_grpc_client import check_inventory, reduce_stock
from models.order import save_order
import logging

logger = logging.getLogger(__name__)

class OrderServiceServicer(order_pb2_grpc.OrderServiceServicer):
    async def CreateOrder(self, request, context):
        product_id = request.product_id
        quantity = request.quantity
        client_id = request.client_id

        try:
            has_stock = await check_inventory(product_id, quantity)
            if not has_stock:
                logger.warning(f"Insufficient stock for product {product_id}, quantity requested: {quantity}")
                return order_pb2.OrderResponse(success=False, message="Insufficient stock.")

            ok = await reduce_stock(product_id, quantity)
            if not ok:
                logger.warning(f"Failed to reduce stock for product {product_id}. Possible race condition or update conflict.")
                return order_pb2.OrderResponse(success=False, message="Could not reduce stock.")

            ok = await save_order(product_id, quantity, client_id)
            if not ok:
                logger.error(f"Failed to save order for product {product_id}, quantity {quantity}, client {client_id}")
                return order_pb2.OrderResponse(success=False, message="Could not save order.")

            logger.info(f"Order created successfully for product {product_id}, quantity {quantity}, client {client_id}")
            return order_pb2.OrderResponse(success=True, message="Order created successfully.")
        except Exception as e:
            logger.error(f"Unexpected error while creating order for product {product_id}: {e}")
            return order_pb2.OrderResponse(success=False, message="Internal error.")
