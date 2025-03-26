import uvicorn
from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from config.limiter import limiter
from core.router import dynamic_route

app = FastAPI(title="API Gateway")

# Configuración global de rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Endpoint catch-all para manejar todas las rutas
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@limiter.limit("60/minute")
async def catch_all(request: Request, full_path: str):
    return await dynamic_route(request, full_path)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
