# inventory_service/consumers/queue_consumer.py

import json
import logging
import asyncio
import os
from aio_pika import connect_robust
from dotenv import load_dotenv
from config.database import inventory_collection
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("INVENTORY_QUEUE_NAME", "inventory_queue")  

async def process_message(message):
    async with message.process():
        try:
            data = json.loads(message.body)
            logger.info(f"Received failover message: {data}")

            if data.get("operation") == "check_inventory":
                product_id = data.get("product_id")
                client_id = data.get("client_id")
                logger.info(f"Recovering check_inventory for product {product_id}, client {client_id}")
        except Exception as e:
            logger.error(f"Error processing inventory failover message: {str(e)}")

async def start_inventory_consumer():
    max_retries = 10
    retry_delay = 5

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[RabbitMQ] Connecting attempt {attempt} to {RABBITMQ_URL}")
            connection = await connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            queue = await channel.declare_queue(QUEUE_NAME, durable=True)
            await queue.consume(process_message)
            logger.info("Connected and listening for inventory failover messages.")
            await asyncio.Future()  
            break
        except Exception as e:
            logger.warning(f"Retry {attempt} failed: {str(e)}")
            if attempt == max_retries:
                logger.error("Could not connect after multiple attempts.")
            await asyncio.sleep(retry_delay)
