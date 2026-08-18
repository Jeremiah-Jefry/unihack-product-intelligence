"""Health and readiness check endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.health import HealthResponse, ReadyResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Liveness check — confirms the service is running."""
    return HealthResponse(
        status="ok",
        service="product-intelligence-api",
        version="0.1.0",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/ready", response_model=ReadyResponse)
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check — confirms dependencies are available."""
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unavailable"

    status = "ready" if db_status == "ok" else "not_ready"

    return ReadyResponse(
        status=status,
        database=db_status,
        timestamp=datetime.now(timezone.utc),
    )
