# api-gateway/routes/product.py
from fastapi import APIRouter, Query, Request
from models.product import ProductResponse, ProductsResponse
from methods.product import get_products_grpc_fallback as get_products_grpc
from config.limiter import limiter

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=ProductsResponse)
@limiter.limit("60/minute")
async def get_products(request: Request, page: int = Query(1), limit: int = Query(12), client_id: str = Query(None)):
    products = await get_products_grpc(client_id)
    total = len(products)
    start = (page - 1) * limit
    end = start + limit
    paginated = products[start:end]
    return {
        "products": paginated,
        "total": total,
        "page": page,
        "limit": limit
    }
