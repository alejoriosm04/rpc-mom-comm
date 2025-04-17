# config/grpc.py
from pb import order_pb2_grpc
from methods.order import OrderServiceServicer
import grpc
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
grpc_port = os.getenv("GRPC_SERVER_PORT", "50053")

async def serve():
    server = grpc.aio.server()
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServiceServicer(), server)
    server.add_insecure_port(f"[::]:{grpc_port}")
    await server.start()
    print(f"OrderService gRPC listening to port: {grpc_port}")
    await server.wait_for_termination()
