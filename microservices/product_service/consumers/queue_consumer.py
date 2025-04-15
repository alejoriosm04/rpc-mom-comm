import json
import logging
import aiohttp
import os
from dotenv import load_dotenv
from aio_pika import connect_robust
from config.database import products_collection

logger = logging.getLogger(__name__)

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "product_queue")

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
                            "http://localhost:8000/push/products",
                            json={"client_id": client_id, "products": products}
                        )
        except Exception as e:
            logger.error(f"Error procesando mensaje de cola: {str(e)}")

async def start_consumer():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(process_message)
    logger.info("Consumidor RabbitMQ activo y escuchando.")
