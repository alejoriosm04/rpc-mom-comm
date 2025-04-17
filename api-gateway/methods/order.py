import logging
import grpc.aio
from config.grpc import get_order_stub
from pb import order_pb2
from grpc import StatusCode
from methods.queue import enqueue_order_request  # Asegúrate de tener esta función

logger = logging.getLogger(__name__)

async def create_order_grpc(product_id: int, quantity: int, client_id: str):
    try:
        stub = get_order_stub()
        request = order_pb2.OrderRequest(
            product_id=product_id,
            quantity=quantity,
            client_id=client_id
        )
        response = await stub.CreateOrder(request)
        logger.info("gRPC call to CreateOrder succeeded.")
        return {
            "success": response.success,
            "message": response.message
        }
    
    except grpc.aio.AioRpcError as e:
        logger.error(f"gRPC call to CreateOrder failed: {e}")
        if e.code() == StatusCode.UNAVAILABLE:
            logger.warning("Order microservice is unavailable. Sending request to RabbitMQ queue.")
            await enqueue_order_request({
                "operation": "create_order",
                "product_id": product_id,
                "quantity": quantity,
                "client_id": client_id
            })
            return {
                "success": False,
                "message": "Order service is currently unavailable. Request has been queued."
            }

        return {
            "success": False,
            "message": "Unexpected error occurred while processing the order."
        }
