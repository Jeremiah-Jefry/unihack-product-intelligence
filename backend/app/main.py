"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import AppError, DependencyError, NotFoundError, ValidationError
from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    setup_logging()
    logger.info("Starting Product Intelligence API", extra={"env": settings.APP_ENV})

    # Ensure data directories exist
    import os
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)

    yield

    logger.info("Shutting down Product Intelligence API")
    engine.dispose()


app = FastAPI(
    title="Product Intelligence API",
    description="AI-Powered Product Intelligence for Industrial Commerce",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

# CORS — restricted for development, configurable for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:8501",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


# --- Exception handlers ---


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "not_found", "message": exc.message, "details": exc.details},
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "message": exc.message, "details": exc.details},
    )


@app.exception_handler(DependencyError)
async def dependency_error_handler(request: Request, exc: DependencyError):
    return JSONResponse(
        status_code=503,
        content={"error": "dependency_unavailable", "message": exc.message, "details": exc.details},
    )


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "message": exc.message, "details": exc.details},
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "message": "An unexpected error occurred"},
    )
