"""
API routes package — health check endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Backend health check",
)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        gemini_model=settings.GEMINI_MODEL,
    )
