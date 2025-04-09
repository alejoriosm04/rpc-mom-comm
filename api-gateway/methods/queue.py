# api-gateway/methods/queue.py
import json
from aio_pika import Message
from config.rabbitmq import get_rabbitmq_connection

QUEUE_NAME = "product_requests"

async def enqueue_product_request(payload: dict):
    print("Enqueuing request:", payload)
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(QUEUE_NAME, durable=True)

        message = Message(json.dumps(payload).encode())
        await channel.default_exchange.publish(
            message,
            routing_key=QUEUE_NAME,
        )
