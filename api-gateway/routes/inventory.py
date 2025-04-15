# api-gateway/routes/inventory.py
from fastapi import APIRouter, Query, Request
from methods.inventory import check_inventory_grpc
from config.limiter import limiter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

@router.get("/check")
@limiter.limit("60/minute")
async def check_inventory(
    request: Request,
    product_id: int = Query(...),
    client_id: str = Query(None)
):
    result = await check_inventory_grpc(product_id, client_id)
    return JSONResponse(content=result)
