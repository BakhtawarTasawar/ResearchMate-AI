
"""
Gemini client service.
Initialises and exposes a cached Google GenAI client.
"""
from __future__ import annotations

from functools import lru_cache

from google import genai
from google.genai import types

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_gemini_client() -> genai.Client:
    """Return a cached Gemini client, initialised once."""

    settings = get_settings()

    logger.info(
        "Initialising Gemini client (model=%s)",
        settings.GEMINI_MODEL,
    )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY,
        http_options=types.HttpOptions(
            timeout=settings.GEMINI_TIMEOUT_SECONDS * 1000,
        ),
    )
