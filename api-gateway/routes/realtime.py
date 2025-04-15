# api-gateway/methods/realtime.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

router = APIRouter()
connected_clients = {}

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
async def push_products(data: dict):
    client_id = data.get("client_id")
    payload = data.get("products")
    websocket = connected_clients.get(client_id)
    if websocket:
        await websocket.send_json({"products": payload})
        return JSONResponse(content={"status": "ok"})
    return JSONResponse(content={"error": "client not connected"}, status_code=404)
