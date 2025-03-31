import logging
import grpc.aio
from config.grpc import get_product_stub
from pb import product_pb2
from services.rabbitmq_service import publish_to_rabbitmq

logger = logging.getLogger(__name__)

async def get_products_grpc():
    try:
        stub = get_product_stub()
        request = product_pb2.ProductRequest()
        response = await stub.GetProducts(request)
        logger.info("Llamada gRPC a GetProducts exitosa.")
        return _format_products(response.products)

    except grpc.aio.AioRpcError as e:
        logger.error(f"Error en gRPC. Encolando en RabbitMQ: {e}")
        # Publicar mensaje de fallo en RabbitMQ para reprocesamiento
        publish_to_rabbitmq({"action": "get_products", "retry_count": 0})
        return []

def _format_products(products):
    return [{
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
    } for product in products] 
