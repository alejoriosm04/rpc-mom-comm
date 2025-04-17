import grpc
import os
from dotenv import load_dotenv
from pb import product_pb2_grpc

load_dotenv()

def get_product_stub():
    host = os.getenv("PRODUCT_SERVER_HOST", "product_service")
    port = os.getenv("PRODUCT_SERVER_PORT", "50051")
    channel = grpc.aio.insecure_channel(f"{host}:{port}")
    return product_pb2_grpc.ProductServiceStub(channel)
