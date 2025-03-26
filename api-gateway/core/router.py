import json
from fastapi import Request, HTTPException, Response
from methods.product import get_products_grpc

async def dynamic_route(request: Request, full_path: str) -> Response:
    normalized_path = full_path.strip("/")
    
    if normalized_path == "products" and request.method.upper() == "GET":
        products = await get_products_grpc()
        content = json.dumps(products)
        return Response(content=content, media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="Route not found")
