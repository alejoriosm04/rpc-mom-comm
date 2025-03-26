import os
from dotenv import load_dotenv
import grpc
from concurrent import futures
from pb import product_pb2_grpc
from config.grpc import ProductServiceServicer

load_dotenv()
grpc_port = os.getenv("GRPC_SERVER_PORT")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    server.start()
    print(f"ProductService running on port {grpc_port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
