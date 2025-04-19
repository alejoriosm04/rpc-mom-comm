import json
import logging
import aiohttp
import os
import asyncio
from aio_pika import connect_robust
from dotenv import load_dotenv
from methods.order import OrderServiceServicer
from pb import order_pb2
from pb import product_pb2_grpc, product_pb2
import grpc.aio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "order_queue")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")
PRODUCT_SERVER_HOST = os.getenv("PRODUCT_SERVER_HOST", "product_service")
PRODUCT_SERVER_PORT = os.getenv("PRODUCT_SERVER_PORT", "50051")


async def get_updated_products():
    try:
        async with grpc.aio.insecure_channel(f"{PRODUCT_SERVER_HOST}:{PRODUCT_SERVER_PORT}") as channel:
            stub = product_pb2_grpc.ProductServiceStub(channel)
            response = await stub.GetProducts(product_pb2.ProductRequest())  # Ajusta si usas otro request
            products = [
                {
                    "id": product.id,
                    "title": product.title,
                    "description": product.description,
                    "price": product.price,
                    "stock": product.stock,
                    "images": list(product.images),
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name,
                        "image": product.category.image,
                        "slug": product.category.slug
                    }
                }
                for product in response.products
            ]
            return products
    except Exception as e:
        logger.warning(f"⚠️ Failed to fetch updated products: {e}")
        return []


async def process_message(message):
    async with message.process():
        try:
            data = json.loads(message.body)

            if data.get("operation") == "create_order":
                logger.info("📦 Processing order from queue...")

                product_id = int(data.get("product_id"))
                quantity = int(data.get("quantity"))
                client_id = str(data.get("client_id"))

                request = order_pb2.OrderRequest(
                    product_id=product_id,
                    quantity=quantity,
                    client_id=client_id
                )

                service = OrderServiceServicer()
                response = await service.CreateOrder(request, context=None)

                async with aiohttp.ClientSession() as session:
                    # Notificar estado de orden
                    await session.post(
                        f"{API_GATEWAY_URL}/push/orders",
                        json={
                            "client_id": client_id,
                            "status": "confirmed" if response.success else "rejected",
                            "product_id": product_id,
                            "quantity": quantity,
                            "message": "Your order has been confirmed." if response.success else "Order rejected."
                        }
                    )
                    logger.info("📨 Order status pushed to gateway.")

                    if response.success:
                        logger.info("✅ Order processed, fetching updated products...")
                        updated_products = await get_updated_products()

                        await session.post(
                            f"{API_GATEWAY_URL}/push/products",
                            json={
                                "client_id": client_id,
                                "products": updated_products
                            }
                        )
                        logger.info("✅ Updated products pushed to client.")

        except Exception as e:
            logger.error(f"🔥 Error processing RabbitMQ message: {str(e)}")


async def start_consumer():
    max_retries = 30
    retry_delay = 3

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[RabbitMQ] Attempt {attempt}: connecting to {RABBITMQ_URL}")
            connection = await connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            queue = await channel.declare_queue(QUEUE_NAME, durable=True)
            await queue.consume(process_message)
            logger.info("[RabbitMQ] Connected and consuming.")
            await asyncio.Future()
            break
        except Exception as e:
            logger.warning(f"[RabbitMQ] Connection failed (attempt {attempt}): {str(e)}")
            if attempt == max_retries:
                logger.error("[RabbitMQ] Failed to connect after multiple attempts.")
                raise e
            await asyncio.sleep(retry_delay)
