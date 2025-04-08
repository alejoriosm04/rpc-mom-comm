import json
import pika
from config.rabbitmq import get_rabbitmq_connection, RABBITMQ_QUEUE

def publish_to_rabbitmq(message: dict):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistencia
        )
        connection.close()
        return True
    except Exception as e:
        print(f"Error al publicar en RabbitMQ: {e}")
        return False