import json
import logging
import aiohttp
import os
from dotenv import load_dotenv
from aio_pika import connect_robust
from config.database import products_collection
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "product_queue")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

async def process_message(message):
    async with message.process():
        try:
            data = json.loads(message.body)
            if data.get("operation") == "get_products":
                logger.info("Procesando operación encolada: get_products")
                products = []
                cursor = products_collection.find()
                async for doc in cursor:
                    if "_id" in doc:
                        doc["_id"] = str(doc["_id"])
                    products.append(doc)
                logger.info("Productos procesados desde cola.")

                client_id = data.get("client_id")
                if client_id:
                    logger.info(f"Enviando productos al cliente {client_id} vía API Gateway.")
                    async with aiohttp.ClientSession() as session:
                        await session.post(
                            f"{API_GATEWAY_URL}/push/products",
                            json={"client_id": client_id, "products": products}
                        )
        except Exception as e:
            logger.error(f"Error procesando mensaje de cola: {str(e)}")

async def start_consumer():
    max_retries = 10
    retry_delay = 5  

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[RabbitMQ] Intento {attempt}: conectando a {RABBITMQ_URL}")
            connection = await connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            queue = await channel.declare_queue(QUEUE_NAME, durable=True, auto_delete=False, passive=False)

            await queue.consume(process_message)
            logger.info("[RabbitMQ] Conexión exitosa. Consumidor activo.")
            break
        except Exception as e:
            logger.warning(f"[RabbitMQ] Fallo en el intento {attempt}: {str(e)}")
            if attempt == max_retries:
                logger.error("[RabbitMQ] No se pudo conectar tras múltiples intentos. Abortando.")
                raise e
            await asyncio.sleep(retry_delay)

