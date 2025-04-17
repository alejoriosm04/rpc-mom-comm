import grpc
import os
from dotenv import load_dotenv

from pb import product_pb2_grpc
from pb import inventory_pb2_grpc
from pb import order_pb2_grpc 

load_dotenv()

# Product microservice stub
def get_product_stub():
    host = os.getenv("PRODUCT_SERVER_HOST", "localhost")
    port = os.getenv("PRODUCT_SERVER_PORT", "50051")
    channel = grpc.aio.insecure_channel(f"{host}:{port}")
    return product_pb2_grpc.ProductServiceStub(channel)

def get_inventory_stub():
    host = os.getenv("INVENTORY_SERVER_HOST", "localhost")
    port = os.getenv("INVENTORY_SERVER_PORT", "50052")
    channel = grpc.aio.insecure_channel(f"{host}:{port}")
    return inventory_pb2_grpc.InventoryServiceStub(channel)

def get_order_stub():
    host = os.getenv("ORDER_SERVER_HOST", "localhost")
    port = os.getenv("ORDER_SERVER_PORT", "50053")
    channel = grpc.aio.insecure_channel(f"{host}:{port}")
    return order_pb2_grpc.OrderServiceStub(channel)