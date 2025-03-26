from fastapi import APIRouter, Depends, Request
from models.product import ProductResponse
from methods.product import get_products
from slowapi.util import get_remote_address
from config.limiter import limiter  

router = APIRouter()

@router.get(
    "/products",
    response_model=list[ProductResponse],
    tags=["Products"],
)
@limiter.limit("60/minute") 
async def products(request: Request):  
    return get_products()
