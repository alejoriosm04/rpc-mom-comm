from fastapi import FastAPI
from routes import product
from slowapi.errors import RateLimitExceeded
from config.limiter import limiter, _rate_limit_exceeded_handler

app = FastAPI(title="API Gateway")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(product.router)
