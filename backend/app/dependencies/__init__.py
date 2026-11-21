
"""
FastAPI dependency injection helpers.
"""
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.core.security import decode_access_token

from app.services.research_service import (
    ResearchAnalysisService,
    get_research_service,
)
from app.services.extraction_service import (
    DocumentExtractionService,
    get_extraction_service,
)


bearer_scheme = HTTPBearer(auto_error=False)


def research_service_dep() -> ResearchAnalysisService:
    return get_research_service()


def extraction_service_dep() -> DocumentExtractionService:
    return get_extraction_service()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except Exception:
        raise unauthorized

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise unauthorized

    return user
