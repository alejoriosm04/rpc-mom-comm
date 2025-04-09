import json
import logging
from aio_pika import connect_robust
from config.database import products_collection

logger = logging.getLogger(__name__)

RABBITMQ_URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "product_requests"

async def process_message(message):
    async with message.process():
        try:
            data = json.loads(message.body)
            if data.get("operation") == "get_products":
                logger.info("Procesando operación encolada: get_products")
                cursor = products_collection.find()
                async for doc in cursor:
                    logger.debug(f"Producto: {doc}")
                logger.info("Productos procesados desde cola.")
            # Agrega más operaciones si lo necesitas
        except Exception as e:
            logger.error(f"Error procesando mensaje de cola: {str(e)}")

async def start_consumer():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(process_message)
    logger.info("Consumidor RabbitMQ activo y escuchando.")
