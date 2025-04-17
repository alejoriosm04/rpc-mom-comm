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

        logger.info(f"Checking inventory for product {product_id} with quantity {quantity}")
        has_stock = await check_inventory(product_id, quantity)
        if not has_stock:
            logger.warning("Not enough stock available.")
            return order_pb2.OrderResponse(
                success=False,
                message="Insufficient stock available in inventory."
            )

        logger.info("Stock available. Proceeding to create order.")
        await save_order(product_id, quantity, client_id)

        logger.info("Reducing stock...")
        stock_reduced = await reduce_stock(product_id, quantity)
        if not stock_reduced:
            logger.warning("Stock could not be reduced (possible race condition).")

        return order_pb2.OrderResponse(
            success=True,
            message="Order created successfully."
        )
