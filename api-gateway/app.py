# api-gateway/app.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import product, realtime, inventory, order
from slowapi.errors import RateLimitExceeded
from config.limiter import limiter, _rate_limit_exceeded_handler
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="API Gateway",
    version="1.0.0",
    description="Gateway for product, inventory, and order microservices with API Key authentication",
    openapi_tags=[
        {"name": "Products", "description": "Operations related to products"},
        {"name": "Inventory", "description": "Operations related to inventory"},
        {"name": "Orders", "description": "Order creation and management"},
    ]
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routers
app.include_router(product.router)
app.include_router(inventory.router)
app.include_router(order.router)
app.include_router(realtime.router)

# Override OpenAPI for API Key Auth in Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags
    )

    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key"
        }
    }
    openapi_schema["security"] = [{"APIKeyHeader": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
