from pb import inventory_pb2, inventory_pb2_grpc
import os
import grpc
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("INVENTORY_SERVER_HOST", "inventory_service")
port = os.getenv("INVENTORY_SERVER_PORT", "50052")

async def check_inventory(product_id: int, quantity: int):
    async with grpc.aio.insecure_channel(f"{host}:{port}") as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        request = inventory_pb2.InventoryRequest(product_id=product_id)
        response = await stub.CheckInventory(request)
        return response.available and response.stock >= quantity

async def reduce_stock(product_id: int, quantity: int):
    async with grpc.aio.insecure_channel(f"{host}:{port}") as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        request = inventory_pb2.InventoryUpdateRequest(product_id=product_id, quantity=quantity)
        response = await stub.ReduceStock(request)
        return response.success
