"""Initial database models — minimal operational table for connectivity verification."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class HealthCheck(Base):
    """Minimal table to verify database connectivity and migration state."""
    __tablename__ = "health_check"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), nullable=False, default="ok")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
