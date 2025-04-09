from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import product
from slowapi.errors import RateLimitExceeded
from config.limiter import limiter, _rate_limit_exceeded_handler

app = FastAPI(title="API Gateway")

# WebSocket connection pool
connected_clients = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connected_clients[client_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # keep the connection open
    except WebSocketDisconnect:
        connected_clients.pop(client_id, None)

@app.post("/push/products")
async def push_products(data: dict):
    client_id = data.get("client_id")
    payload = data.get("products")
    websocket = connected_clients.get(client_id)
    if websocket:
        await websocket.send_json({"products": payload})
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(product.router)
