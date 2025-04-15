import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import grpc
from pb import inventory_pb2_grpc, inventory_pb2

async def run():
    async with grpc.aio.insecure_channel('localhost:50052') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        response = await stub.CheckInventory(inventory_pb2.InventoryRequest(product_id=1))
        print(f"Available: {response.available}, Stock: {response.stock}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(run())
