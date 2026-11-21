
"""
Core configuration for ResearchGate AI backend.
Loads and validates environment variables.
"""
from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite",
    )

    # Generation settings
    GEMINI_TEMPERATURE: float = float(
        os.getenv("GEMINI_TEMPERATURE", "0.2")
    )
    GEMINI_MAX_OUTPUT_TOKENS: int = int(
        os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "8192")
    )
    GEMINI_TIMEOUT_SECONDS: int = int(
        os.getenv("GEMINI_TIMEOUT_SECONDS", "90")
    )

    # Analysis settings
    MAX_UPLOAD_BYTES: int = 10 * 1024 * 1024
    MAX_TEXT_CHARS: int = 100_000
    MIN_TEXT_CHARS: int = 50

    # Server
    APP_TITLE: str = "ResearchGate AI"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = (
        "Scientific research assistant backend powered by Google Gemini."
    )
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    FRONTEND_URL: str = os.getenv(
        "FRONTEND_URL",
        "http://localhost:8501",
    )

    def validate(self) -> None:
        """Validate critical environment variables."""
        if not self.GEMINI_API_KEY:
            raise EnvironmentError(
                "GEMINI_API_KEY is not set. Add it to backend/.env"
            )

        if not 0 <= self.GEMINI_TEMPERATURE <= 2:
            raise ValueError(
                "GEMINI_TEMPERATURE must be between 0 and 2."
            )

        if self.GEMINI_MAX_OUTPUT_TOKENS <= 0:
            raise ValueError(
                "GEMINI_MAX_OUTPUT_TOKENS must be positive."
            )

        if self.GEMINI_TIMEOUT_SECONDS <= 0:
            raise ValueError(
                "GEMINI_TIMEOUT_SECONDS must be positive."
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.validate()
    return settings
