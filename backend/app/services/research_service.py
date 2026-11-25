
"""
Research analysis service.

Handles prompt construction, Gemini structured generation,
response parsing, and Pydantic validation.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.research import AnalysisResult
from app.services.gemini_client import get_gemini_client
from app.services.prompts import ANALYSIS_PROMPT_TEMPLATE
from google.genai import errors as genai_errors

try:
    import httpx
except ImportError:
    try:
        import httpx2 as httpx
    except ImportError:
        httpx = None

logger = get_logger(__name__)

MAX_ATTEMPTS: int = 3
RETRY_DELAYS: tuple[float, ...] = (2.0, 4.0)


class ResearchAnalysisService:
    """Analyse scientific research text using Gemini."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._client = get_gemini_client()

    def analyse(self, text: str) -> AnalysisResult:
        text = text.strip()

        if len(text) < self._settings.MIN_TEXT_CHARS:
            raise ValueError(
                f"Input text is too short ({len(text)} characters). "
                f"Minimum required: {self._settings.MIN_TEXT_CHARS}."
            )

        if len(text) > self._settings.MAX_TEXT_CHARS:
            raise ValueError(
                f"Input text exceeds the maximum limit of "
                f"{self._settings.MAX_TEXT_CHARS} characters."
            )

        # Replace only the text placeholder.
        # This avoids conflicts with JSON braces inside the prompt.
        prompt = ANALYSIS_PROMPT_TEMPLATE.replace("{text}", text)

        logger.info(
            "Starting research analysis | model=%s | characters=%d",
            self._settings.GEMINI_MODEL,
            len(text),
        )

        response = None
        last_error: Exception | None = None

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                logger.info(
                    "Calling Gemini API | model=%s | attempt=%d/%d",
                    self._settings.GEMINI_MODEL,
                    attempt,
                    MAX_ATTEMPTS,
                )
                response = self._client.models.generate_content(
                    model=self._settings.GEMINI_MODEL,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": AnalysisResult,
                        "temperature": 0.2,
                    },
                )
                break
            except Exception as exc:
                last_error = exc
                if attempt < MAX_ATTEMPTS and self._is_temporary_error(exc):
                    delay = RETRY_DELAYS[attempt - 1]
                    logger.warning(
                        "Temporary Gemini error on attempt %d/%d (code=%s): %s. Retrying in %.1fs...",
                        attempt,
                        MAX_ATTEMPTS,
                        getattr(exc, "code", None),
                        exc,
                        delay,
                    )
                    time.sleep(delay)
                else:
                    if not self._is_temporary_error(exc):
                        logger.error(
                            "Permanent or non-retryable Gemini error on attempt %d (code=%s): %s",
                            attempt,
                            getattr(exc, "code", None),
                            exc,
                        )
                    else:
                        logger.error(
                            "Gemini generation failed after %d attempts: %s",
                            MAX_ATTEMPTS,
                            exc,
                        )
                    break

        if response is None:
            logger.exception("Gemini generation failed permanently or exhausted all attempts", exc_info=last_error)

            if isinstance(last_error, genai_errors.APIError) and last_error.code in {429, 503}:
                raise RuntimeError(
                    "The AI analysis service is currently experiencing high demand. "
                    "Please try again in a few moments."
                ) from last_error

            raise RuntimeError(
                "The AI analysis service could not complete your request. "
                "Please check your Gemini API configuration and try again."
            ) from last_error

        raw = response.text

        if not raw or not raw.strip():
            raise ValueError(
                "Gemini returned an empty response. "
                "Please try again with a different research document."
            )

        logger.info(
            "Gemini response received | response_characters=%d",
            len(raw),
        )

        parsed = self._parse_json(raw)

        result = self._validate_result(parsed)

        logger.info("Research analysis completed successfully")

        return result

    @staticmethod
    def _is_temporary_error(exc: Exception) -> bool:
        """
        Determine if an exception represents a temporary, retryable error.

        Temporary errors:
        - HTTP 503 (Service Unavailable / High Demand)
        - HTTP 429 (Rate Limit / Resource Exhausted)
        - HTTP 500, 502, 504 (Server-side transient failures)
        - Network/connection timeouts and transport errors

        Permanent errors (HTTP 400, 401, 403, 404, etc.) are never retried.
        """
        if isinstance(exc, genai_errors.APIError):
            if exc.code in {429, 500, 502, 503, 504}:
                return True
            if isinstance(exc, genai_errors.ServerError):
                return True
            return False

        if isinstance(exc, (ConnectionError, TimeoutError)):
            return True

        if httpx is not None and isinstance(exc, (httpx.TimeoutException, httpx.ConnectError)):
            return True

        return False

    @staticmethod
    def _strip_code_fences(text: str) -> str:
        """Remove Markdown code fences if the model returns them."""

        return re.sub(
            r"^\s*```(?:json)?\s*|\s*```\s*$",
            "",
            text.strip(),
            flags=re.IGNORECASE,
        ).strip()

    def _parse_json(self, raw: str) -> dict[str, Any]:
        """Parse the Gemini response into a JSON object."""

        clean = self._strip_code_fences(raw)

        try:
            parsed = json.loads(clean)

        except json.JSONDecodeError as exc:
            logger.error(
                "Invalid JSON returned by Gemini. Response: %.500s",
                raw,
            )

            raise ValueError(
                "The AI returned an invalid response format. "
                "Please run the analysis again."
            ) from exc

        if not isinstance(parsed, dict):
            raise ValueError(
                "The AI returned an unexpected response format."
            )

        return parsed

    @staticmethod
    def _validate_result(data: dict[str, Any]) -> AnalysisResult:
        """Validate the response against the application schema."""

        try:
            return AnalysisResult.model_validate(data)

        except Exception as exc:
            logger.error(
                "Gemini response failed schema validation: %s",
                exc,
            )

            raise ValueError(
                "The AI response did not match the required research "
                "analysis structure. Please try again."
            ) from exc


_service: ResearchAnalysisService | None = None


def get_research_service() -> ResearchAnalysisService:
    """Return the shared research analysis service."""

    global _service

    if _service is None:
        _service = ResearchAnalysisService()

    return _service
