"""Health check schemas for API responses."""

from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response for GET /health"""

    status: str = "ok"
    service: str = "product-intelligence-api"
    version: str = "0.1.0"
    timestamp: datetime


class ReadyResponse(BaseModel):
    """Response for GET /ready"""

    status: str = "ready"
    database: str = "ok"
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    message: str
    details: dict | list | None = None
