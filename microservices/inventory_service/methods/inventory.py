from config.product_grpc_client import get_product_stub
from pb import product_pb2

async def check_inventory(product_id: int):
    stub = get_product_stub()

    # Aquí puedes cambiar por ProductByIdRequest si existe
    request = product_pb2.ProductRequest()
    response = await stub.GetProducts(request)

    product = next((p for p in response.products if p.id == product_id), None)

    if not product:
        return {"available": False, "stock": 0}

    # Si lo encuentra, simula que hay stock
    return {
        "available": True,
        "stock": 25,  # Simulado
        "product_title": product.title
    }
