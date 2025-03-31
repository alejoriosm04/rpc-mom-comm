import logging
import grpc.aio
from config.grpc import get_product_stub
from pb import product_pb2

logger = logging.getLogger(__name__)

async def get_products_grpc():
    try:
        stub = get_product_stub()
        request = product_pb2.ProductRequest()
        response = await stub.GetProducts(request)
        logger.info("Llamada gRPC a GetProducts exitosa.")
    except grpc.aio.AioRpcError as e:
        logger.error(f"Error en gRPC: {e}")
        return []

    products_list = []
    for product in response.products:
        products_list.append({
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "description": product.description,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
                "image": product.category.image,
                "slug": product.category.slug
            },
            "images": list(product.images)
        })
    return products_list    
