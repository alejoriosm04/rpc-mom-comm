from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from prometheus_client.exposition import basic_auth_handler
import time
from fastapi import Request, Response

# Request count metric: Count the total number of requests hitting the gateway
gateway_requests_total = Counter(
    "gateway_requests_total",
    "Total number of requests to the API Gateway"
)

# Request latency metric: Measure the duration of each request
gateway_request_duration_seconds = Histogram(
    "gateway_request_duration_seconds",
    "Histogram of request durations to the API Gateway",
    ["method", "endpoint"]
)

# Request status code count metric: Track status codes (e.g., 200, 500, etc.)
gateway_status_codes_total = Counter(
    "gateway_status_codes_total",
    "Total number of requests by HTTP status code",
    ["status_code"]
)

def record_request_metrics(request: Request, response_time: float, status_code: int):
    method = request.method
    endpoint = request.url.path
    
    # Record request count
    gateway_requests_total.inc()

    # Record request duration
    gateway_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(response_time)

    # Record status code count
    gateway_status_codes_total.labels(status_code=str(status_code)).inc()

def expose_metrics():
    from fastapi import APIRouter
    router = APIRouter()

    @router.get("/metrics")
    async def metrics():
        # Expose metrics in the format that Prometheus expects
        return Response(generate_latest(REGISTRY), media_type="text/plain; version=0.0.4")

    return router
