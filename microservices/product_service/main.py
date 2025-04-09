# microservices/product_service/main.py
import os
from dotenv import load_dotenv
import grpc
import asyncio
from concurrent import futures
from pb import product_pb2_grpc
from config.grpc import ProductServiceServicer
from consumers.queue_consumer import start_consumer  # <- Nuevo

load_dotenv()
grpc_port = os.getenv("GRPC_SERVER_PORT")

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    await server.start()
    print(f"ProductService running on port {grpc_port}")

    # Iniciar consumidor RabbitMQ en paralelo
    await asyncio.gather(server.wait_for_termination(), start_consumer())

if __name__ == '__main__':
    asyncio.run(serve())
