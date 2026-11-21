from app.api.routes.health import router as health_router
from app.api.routes.research import router as research_router
from app.api.routes.auth import router as auth_router

__all__ = [
    "health_router",
    "research_router",
    "auth_router",
]