"""
ResearchGate AI — FastAPI application entry point.

Start with:
    cd backend
    uvicorn app.main:app --reload --port 8000

Swagger UI: http://localhost:8000/docs
"""
from __future__ import annotations

import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes.auth import router as auth_router
from app.api.routes import health_router, research_router, auth_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

configure_logging(logging.INFO)
logger = get_logger(__name__)

try:
    settings = get_settings()
except EnvironmentError as exc:
    logger.critical("Configuration error at startup: %s", exc)
    raise SystemExit(1) from exc


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "ResearchGate AI backend v%s started — model: %s — CORS: %s",
        settings.APP_VERSION,
        settings.GEMINI_MODEL,
        settings.FRONTEND_URL,
    )
    yield
    logger.info("ResearchGate AI backend shutting down.")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Global exception handler — never leak stack traces to clients
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again.",
        },
    )

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

API_PREFIX = settings.API_V1_PREFIX   # /api/v1

app.include_router(health_router, prefix=API_PREFIX)
app.include_router(research_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)

