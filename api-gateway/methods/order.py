# api-gateway/methods/order.py
from config.grpc import get_order_stub
from pb import order_pb2

async def create_order_grpc(product_id: int, quantity: int, client_id: str):
    stub = get_order_stub()
    request = order_pb2.OrderRequest(
        product_id=product_id,
        quantity=quantity,
        client_id=client_id
    )
    response = await stub.CreateOrder(request)
    return {
        "success": response.success,
        "message": response.message
    }
