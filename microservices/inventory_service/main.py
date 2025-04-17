# inventory_service/main.py

import os
import grpc
import asyncio
from dotenv import load_dotenv
from concurrent import futures
from pb import inventory_pb2_grpc
from config.grpc import InventoryServiceServicer
from consumers.queue_consumer import start_inventory_consumer

load_dotenv()
grpc_port = os.getenv("GRPC_SERVER_PORT", "50052")

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServiceServicer(), server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    await server.start()
    print(f"✅ InventoryService running on port {grpc_port}")

    await asyncio.gather(
        server.wait_for_termination(),
        start_inventory_consumer()
    )

if __name__ == '__main__':
    asyncio.run(serve())
