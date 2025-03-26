import grpc.aio
from config.grpc import get_product_stub
from pb import product_pb2

async def get_products_grpc():
    stub = get_product_stub()  
    request = product_pb2.GetProductsRequest()
    response = await stub.GetProducts(request)
    
    # Transformar la respuesta gRPC a una lista de diccionarios para REST
    products_list = []
    for product in response.products:
        products_list.append({
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "description": product.description,
            
        })
    return products_list
