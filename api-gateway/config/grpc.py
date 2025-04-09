# api-gateway/config/grpc.py
import grpc
import os
from dotenv import load_dotenv
from pb import product_pb2_grpc

load_dotenv()

def get_product_stub():
    product_host = os.getenv("PRODUCT_SERVER_HOST", "localhost")
    product_port = os.getenv("PRODUCT_SERVER_PORT", "50051")
    channel = grpc.aio.insecure_channel(f"{product_host}:{product_port}")
    stub = product_pb2_grpc.ProductServiceStub(channel)
    return stub
