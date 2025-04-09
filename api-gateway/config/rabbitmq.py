import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)
