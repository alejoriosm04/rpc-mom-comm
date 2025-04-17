# api-gateway/routes/order.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from methods.order import create_order_grpc
from fastapi.responses import JSONResponse
from config.limiter import limiter

router = APIRouter(prefix="/api/orders", tags=["Orders"])

class OrderRequest(BaseModel):
    product_id: int
    quantity: int
    client_id: str

@router.post("/")
@limiter.limit("30/minute")
async def create_order(request: Request, order: OrderRequest):
    result = await create_order_grpc(
        product_id=order.product_id,
        quantity=order.quantity,
        client_id=order.client_id
    )
    return JSONResponse(content=result)
