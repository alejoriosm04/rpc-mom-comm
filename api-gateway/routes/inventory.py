# routes/inventory.py
from fastapi import APIRouter, Query, Request, Depends
from methods.inventory import check_inventory_grpc
from config.limiter import limiter
from models.inventory import InventoryResponse
from auth.auth import validate_api_key

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

@router.get("/check", response_model=InventoryResponse)
@limiter.limit("60/minute")
async def check_inventory(
    request: Request,
    product_id: int = Query(...),
    client_id: str = Query(None),
    _auth: None = Depends(validate_api_key)
):
    return await check_inventory_grpc(product_id, client_id)
