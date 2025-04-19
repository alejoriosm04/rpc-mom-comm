import json
import logging
import aiohttp
import os
from dotenv import load_dotenv
from aio_pika import connect_robust
from config.database import products_collection
from config.inventory_grpc_client import get_inventory_stub  
from pb import inventory_pb2  
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
QUEUE_NAME   = os.getenv("QUEUE_NAME", "product_queue")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

async def process_message(message):
    async with message.process():
        data = json.loads(message.body)
        
        if data.get("operation") == "get_products":
            logger.info("Procesando get_products desde la cola...")
            products = []

            cursor = products_collection.find()
            inventory_stub = get_inventory_stub()  

            async for doc in cursor:
                doc["_id"] = str(doc["_id"])
                
                product_id = doc.get("_id")  
                stock = 0

                if product_id:
                    try:
                        logger.info(f"Consultando stock para producto con ID: {product_id}")
                        response = await inventory_stub.CheckInventory(
                            inventory_pb2.InventoryRequest(product_id=int(product_id))
                        )
                        stock = response.stock 

                        logger.info(f"Stock para producto {product_id}: {stock}")
                    except Exception as e:
                        logger.warning(f"Error fetching stock for product {product_id}: {str(e)}")

                doc["stock"] = stock
                
                logger.info(f"Producto {doc['title']} con stock {doc['stock']}")

                products.append(doc)

            logger.info(f"Enviando los siguientes productos al cliente {data.get('client_id')}: {products}")

            client_id = data.get("client_id")
            if client_id:
                logger.info(f"Enviando productos a {client_id} vía Gateway")
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        f"{API_GATEWAY_URL}/push/products",
                        json={"client_id": client_id, "products": products}
                    )

async def start_consumer():
    max_retries = 10
    retry_delay = 5
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[RabbitMQ] Intento {attempt} conectando a {RABBITMQ_URL}")
            connection = await connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            queue = await channel.declare_queue(
                QUEUE_NAME, durable=True, auto_delete=False
            )
            await queue.consume(process_message)
            logger.info("[RabbitMQ] Consumidor listo")
            break
        except Exception as e:
            logger.warning(f"[RabbitMQ] Fallo intento {attempt}: {e}")
            if attempt == max_retries:
                logger.error("No fue posible conectar al broker")
                raise
            await asyncio.sleep(retry_delay)
