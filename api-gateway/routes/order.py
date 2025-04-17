# routes/order.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from config.limiter import limiter
from models.order import OrderRequest, OrderResponse
from methods.order import create_order_grpc
from auth.auth import validate_api_key

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
@limiter.limit("60/minute")
async def create_order(
    request: Request,
    order: OrderRequest,
    _auth: None = Depends(validate_api_key)
):
    result = await create_order_grpc(
        product_id=order.product_id,
        quantity=order.quantity,
        client_id=order.client_id
    )
    return JSONResponse(content=result)
