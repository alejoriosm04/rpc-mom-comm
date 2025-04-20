# api-gateway/routes/realtime.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

router = APIRouter()
connected_clients: dict[str, WebSocket] = {}


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connected_clients[client_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.pop(client_id, None)


@router.post("/push/products")
async def push_products(payload: dict):
    products = payload.get("products", [])
    broadcast = payload.get("broadcast", False)
    client_id = payload.get("client_id")

    if broadcast:
        for ws in connected_clients.values():
            await ws.send_json({"products": products})
    elif client_id in connected_clients:
        await connected_clients[client_id].send_json({"products": products})
    return {"ok": True}


@router.post("/push/orders")
async def push_order_status(data: dict):
    ws = connected_clients.get(data.get("client_id"))
    if ws:
        await ws.send_json({
            "type": "order_status",
            "product_id": data.get("product_id"),
            "quantity": data.get("quantity"),
            "status": data.get("status"),
            "message": data.get("message")
        })
        return JSONResponse({"status": "sent"})
    return JSONResponse({"error": "client not connected"}, status_code=404)
