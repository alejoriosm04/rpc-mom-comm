import grpc
import os
from dotenv import load_dotenv
from pb import inventory_pb2_grpc

load_dotenv()

def get_inventory_stub():
    host = os.getenv("INVENTORY_SERVER_HOST", "inventory_service")
    port = os.getenv("INVENTORY_SERVER_PORT", "50052")
    channel = grpc.aio.insecure_channel(f"{host}:{port}")
    return inventory_pb2_grpc.InventoryServiceStub(channel)
