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

        logger.info(f"➡️ Verificando inventario para producto {product_id} con cantidad {quantity}")
        has_stock = await check_inventory(product_id, quantity)
        if not has_stock:
            logger.warning("❌ No hay suficiente stock.")
            return order_pb2.OrderResponse(success=False, message="No hay suficiente stock en inventario.")

        logger.info("Stock disponible. Procediendo a crear orden.")
        await save_order(product_id, quantity, client_id)

        logger.info("Descontando stock...")
        stock_reduced = await reduce_stock(product_id, quantity)
        if not stock_reduced:
            logger.warning("No se pudo descontar el stock (posible condición de carrera).")

        return order_pb2.OrderResponse(success=True, message="Orden creada exitosamente.")
