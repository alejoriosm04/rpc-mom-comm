# api-gateway/auth/auth.py
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY = os.getenv("API_KEY", "my-secret-key")
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
