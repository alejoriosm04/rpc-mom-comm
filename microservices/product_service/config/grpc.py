from pb import product_pb2_grpc, product_pb2
from methods.product import get_products

class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    def GetProducts(self, request, context):
        products_data = get_products()
        products = []

        for prod in products_data:
            products.append(
                product_pb2.Product(
                    id=prod["id"],
                    title=prod["title"],
                    price=prod["price"],
                    description=prod["description"],
                    category=product_pb2.Category(
                        id=prod["category"]["id"],
                        name=prod["category"]["name"],
                        image=prod["category"]["image"],
                        slug=prod["category"]["slug"]
                    ),
                    images=prod["images"]
                )
            )

        return product_pb2.ProductListResponse(products=products)
