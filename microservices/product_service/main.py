import os
from dotenv import load_dotenv
import grpc
import asyncio
from concurrent import futures
from threading import Thread
from pb import product_pb2_grpc
from config.grpc import ProductServiceServicer
from services.rabbitmq_consumer import start_rabbitmq_consumer

load_dotenv()
grpc_port = os.getenv("GRPC_SERVER_PORT")

async def serve():
    # Iniciar servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    server.start()
    print(f"ProductService running on port {grpc_port}")

    # Iniciar consumidor de RabbitMQ en segundo plano
    rabbitmq_thread = Thread(target=start_rabbitmq_consumer, daemon=True)
    rabbitmq_thread.start()

    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
