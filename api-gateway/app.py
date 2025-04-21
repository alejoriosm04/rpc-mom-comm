from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import product, realtime, inventory, order
from slowapi.errors import RateLimitExceeded
from config.limiter import limiter, _rate_limit_exceeded_handler
from fastapi.openapi.utils import get_openapi
from config.metrics import expose_metrics, record_request_metrics
import time

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

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routes
app.include_router(product.router)
app.include_router(inventory.router)
app.include_router(order.router)
app.include_router(realtime.router)

# Integrate Prometheus metrics
app.include_router(expose_metrics())

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

# Middleware for tracking request metrics
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()  # Start the timer

    # Process the request
    response = await call_next(request)

    # Calculate the response time
    response_time = time.time() - start_time

    # Record the metrics
    record_request_metrics(request, response_time, response.status_code)

    return response