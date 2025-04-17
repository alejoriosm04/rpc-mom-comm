import json
import logging
import aiohttp
import os
import asyncio
from aio_pika import connect_robust
from dotenv import load_dotenv
from methods.order import OrderServiceServicer
from pb import order_pb2  # ✅ Importar el mensaje correcto de gRPC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "order_queue")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

async def process_message(message):
    async with message.process():
        try:
            data = json.loads(message.body)

            if data.get("operation") == "create_order":
                logger.info("Procesando orden desde la cola...")

                # Extraer y tipar los campos correctamente
                product_id = int(data.get("product_id"))
                quantity = int(data.get("quantity"))
                client_id = str(data.get("client_id"))

                # ✅ Crear una instancia real del mensaje de gRPC
                request = order_pb2.OrderRequest(
                    product_id=product_id,
                    quantity=quantity,
                    client_id=client_id
                )

                # Usar el servicio como siempre
                service = OrderServiceServicer()
                response = await service.CreateOrder(request, context=None)

                if response.success:
                    logger.info("Orden procesada desde cola correctamente.")
                else:
                    logger.warning(f"Falló al crear la orden desde la cola: {response.message}")
        except Exception as e:
            logger.error(f"Error procesando mensaje de RabbitMQ: {str(e)}")

async def start_consumer():
    max_retries = 30
    retry_delay = 3

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[RabbitMQ] Intento {attempt}: conectando a {RABBITMQ_URL}")
            connection = await connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            queue = await channel.declare_queue(QUEUE_NAME, durable=True)
            await queue.consume(process_message)
            logger.info("[RabbitMQ] Conexión exitosa. Consumidor activo.")
            await asyncio.Future()  
            break
        except Exception as e:
            logger.warning(f"[RabbitMQ] Fallo en el intento {attempt}: {str(e)}")
            if attempt == max_retries:
                logger.error("[RabbitMQ] No se pudo conectar tras múltiples intentos. Abortando.")
                raise e
            await asyncio.sleep(retry_delay)
