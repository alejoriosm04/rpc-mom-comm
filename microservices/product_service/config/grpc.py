from pb import product_pb2_grpc, product_pb2
from methods.product import get_products
import grpc
import json


class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    async def GetProducts(self, request, context):
        try:
            products_data = await get_products()
            products = []

            for prod in products_data:                
                # Ensure all required fields are present and of correct type
                category_data = prod.get("category", {})
                if not isinstance(category_data, dict):
                    continue

                # Convert MongoDB document to gRPC message
                product = product_pb2.Product(
                    id=int(prod.get("_id", 0)),
                    title=str(prod.get("title", "")),
                    price=float(prod.get("price", 0.0)),
                    description=str(prod.get("description", "")),
                    category=product_pb2.Category(
                        id=int(category_data.get("id", 0)),
                        name=str(category_data.get("name", "")),
                        image=str(category_data.get("image", "")),
                        slug=str(category_data.get("slug", ""))
                    ),
                    images=[str(img) for img in prod.get("images", [])]
                )
                products.append(product)

            return product_pb2.ProductListResponse(products=products)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error processing products: {str(e)}")
            return product_pb2.ProductListResponse()
