import json
import pika
from config.grpc import ProductServiceServicer
from methods.product import get_products
from pb import product_pb2

RABBITMQ_QUEUE = "product_queue"

def start_rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            print(f"Mensaje recibido: {message}")

            # Reprocesar la solicitud fallida
            if message.get("action") == "get_products":
                products = get_products()  # Lógica original
                print(f"Productos reprocesados: {products}")

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error al procesar mensaje: {e}")

    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    print("Consumidor de RabbitMQ iniciado...")
    channel.start_consuming()