# api-gateway/methods/product.py
import logging
import grpc.aio
from config.grpc import get_product_stub
from pb import product_pb2
from grpc import StatusCode
from methods.queue import enqueue_product_request

logger = logging.getLogger(__name__)

async def get_products_grpc_fallback(client_id: str = None):
    try:
        stub = get_product_stub()
        request = product_pb2.ProductRequest()
        response = await stub.GetProducts(request)
        logger.info("gRPC call to GetProducts successful.")
    except grpc.aio.AioRpcError as e:
        logger.error(f"gRPC error: {e}")
        if e.code() == StatusCode.UNAVAILABLE:
            logger.warning("Product microservice unavailable. Enqueuing request.")
            await enqueue_product_request({"operation": "get_products", "client_id": client_id})
        return []  # Return empty list in the meantime

    products_list = []
    for product in response.products:
        products_list.append({
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "description": product.description,
            "stock": product.stock,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
                "image": product.category.image,
                "slug": product.category.slug
            },
            "images": list(product.images)
        })

    return products_list
