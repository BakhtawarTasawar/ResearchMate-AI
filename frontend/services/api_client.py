"""
Frontend API client — communicates with the FastAPI backend.
All external exception messages are sanitized to prevent technical data leakage.
"""
from __future__ import annotations

import io
import logging
from typing import Any

import httpx

from config.settings import BACKEND_API_URL

logger = logging.getLogger("researchgate.api_client")


class APIError(Exception):
    """Application API exception with sanitized user-facing messages."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return self.message


def sanitize_error(exc: Exception, action: str = "general") -> str:
    """
    Map raw exceptions and APIErrors to safe, actionable institutional messages.
    Guarantees no backend URLs, ports, hostnames, or tracebacks leak to the UI.
    """
    if isinstance(exc, APIError):
        # Specific HTTP status codes
        if exc.status_code == 401:
            return "Invalid email or password."
        if exc.status_code == 409:
            return "An account with this email already exists."
        if exc.status_code == 403:
            return "Your account is inactive."
        if exc.status_code in (500, 502, 503, 504):
            return "Unable to connect right now. Please try again in a moment."

        # If it's already a safe user-facing message from APIError
        msg = str(exc.message).strip()
        lower_msg = msg.lower()
        if "connect" in lower_msg or "timeout" in lower_msg or "unreachable" in lower_msg:
            return "Unable to connect right now. Please try again in a moment."
        if "invalid email or password" in lower_msg:
            return "Invalid email or password."
        if "already exists" in lower_msg:
            return "An account with this email already exists."
        if "too short" in lower_msg or "at least 50" in lower_msg:
            return "Input text is too short. Please provide at least 50 characters of scientific text."
        if "exceeds" in lower_msg or "limit" in lower_msg:
            return "The submitted document exceeds the maximum allowable length."

        # Any message containing URLs or technical markers is scrubbed
        if any(marker in lower_msg for marker in ("http", "localhost", "127.0.0.1", "port", "traceback", "exception", "json", "endpoint")):
            return "Something went wrong. Please try again later."

        return msg or "Something went wrong. Please try again later."

    # Generic or network exception
    err_str = str(exc).lower()
    if any(marker in err_str for marker in ("connect", "timeout", "network", "unreachable", "refused")):
        return "Unable to connect right now. Please try again in a moment."

    return "Something went wrong. Please try again later."


class ResearchAPIClient:
    def __init__(
        self,
        base_url: str = BACKEND_API_URL,
        timeout: float = 90.0,
        token: str | None = None,
    ):
        self._base = base_url.rstrip("/")
        self._timeout = timeout
        self._token = token

    def set_token(self, token: str | None) -> None:
        self._token = token

    def _headers(self) -> dict[str, str]:
        if self._token:
            return {"Authorization": f"Bearer {self._token}"}
        return {}

    # Authentication

    def register(
        self, full_name: str, email: str, password: str
    ) -> dict[str, Any]:
        return self._post(
            "/auth/register",
            json={
                "full_name": full_name,
                "email": email,
                "password": password,
            },
            authenticated=False,
        )

    def login(self, email: str, password: str) -> dict[str, Any]:
        return self._post(
            "/auth/login",
            json={"email": email, "password": password},
            authenticated=False,
        )

    def get_current_user(self) -> dict[str, Any]:
        return self._get("/auth/me")

    # Health

    def health_check(self) -> dict[str, Any]:
        return self._get("/health", authenticated=False)

    # Research

    def analyze_text(self, text: str) -> dict[str, Any]:
        return self._post(
            "/research/analyze",
            json={"text": text},
        )

    def extract_text(
        self, filename: str, file_bytes: bytes, content_type: str
    ) -> dict[str, Any]:
        files = {"file": (filename, io.BytesIO(file_bytes), content_type)}
        return self._post("/research/extract-text", files=files)

    # HTTP helpers

    def _get(
        self, path: str, authenticated: bool = True
    ) -> dict[str, Any]:
        headers = self._headers() if authenticated else {}
        logger.debug(
            "GET %s [authenticated=%s, has_token=%s, auth_header_attached=%s]",
            path,
            authenticated,
            bool(self._token),
            "Authorization" in headers,
        )
        try:
            response = httpx.get(
                self._base + path,
                timeout=self._timeout,
                headers=headers,
            )
            return self._handle(response)
        except httpx.TimeoutException:
            logger.warning("Request to %s timed out.", path)
            raise APIError("Unable to connect right now. Please try again in a moment.", status_code=504)
        except httpx.ConnectError:
            logger.warning("Connection failure on GET %s.", path)
            raise APIError("Unable to connect right now. Please try again in a moment.", status_code=503)
        except Exception as exc:
            logger.error("Unexpected exception on GET %s: %s", path, type(exc).__name__)
            raise APIError("Something went wrong. Please try again later.", status_code=500)

    def _post(
        self,
        path: str,
        authenticated: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:
        headers = self._headers() if authenticated else {}
        logger.debug(
            "POST %s [authenticated=%s, has_token=%s, auth_header_attached=%s]",
            path,
            authenticated,
            bool(self._token),
            "Authorization" in headers,
        )

        try:
            response = httpx.post(
                self._base + path,
                timeout=self._timeout,
                headers=headers,
                **kwargs,
            )
            return self._handle(response)
        except httpx.TimeoutException:
            logger.warning("Request to %s timed out.", path)
            raise APIError("Unable to connect right now. Please try again in a moment.", status_code=504)
        except httpx.ConnectError:
            logger.warning("Connection failure on POST %s.", path)
            raise APIError("Unable to connect right now. Please try again in a moment.", status_code=503)
        except Exception as exc:
            logger.error("Unexpected exception on POST %s: %s", path, type(exc).__name__)
            raise APIError("Something went wrong. Please try again later.", status_code=500)

    @staticmethod
    def _handle(response: httpx.Response) -> dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            logger.warning("Server returned non-JSON response with status %s", response.status_code)
            raise APIError(
                "Something went wrong. Please try again later.",
                response.status_code,
            )

        if not response.is_success:
            detail = data.get("detail") or data.get("error")
            if isinstance(detail, list):
                detail = "; ".join(
                    str(item.get("msg", item)) for item in detail
                )

            # Scrub technical strings before creating APIError
            detail_str = str(detail or "")
            if response.status_code == 401:
                clean_msg = "Invalid email or password."
            elif response.status_code == 409:
                clean_msg = "An account with this email already exists."
            elif response.status_code == 403:
                clean_msg = "Your account is inactive."
            elif response.status_code == 422:
                clean_msg = detail_str or "Invalid input provided. Please verify the submitted details."
            elif response.status_code >= 500:
                clean_msg = "Something went wrong. Please try again later."
            else:
                clean_msg = detail_str or "Something went wrong. Please try again later."

            # Ensure no URLs or hostnames leak
            if any(marker in clean_msg.lower() for marker in ("http", "localhost", "127.0.0.1", "port")):
                clean_msg = "Something went wrong. Please try again later."

            raise APIError(clean_msg, response.status_code)

        return data


def get_api_client(token: str | None = None) -> ResearchAPIClient:
    """
    Get the API client instance for the current session.

    Resolution order for authentication token:
    1. Explicit `token` argument if provided.
    2. Token stored in Streamlit session state (`session.get_auth_token()`).
    3. Existing token already held by the client instance.

    To guarantee multi-session and multi-user isolation in Streamlit, clients
    are cached per-session in `st.session_state`. When called outside a Streamlit
    context (e.g. backend unit tests, CLI scripts), a new client instance is returned.
    """
    # 1. Fallback to session token if not explicitly provided
    resolved_token = token
    if resolved_token is None:
        try:
            from utils import session
            resolved_token = session.get_auth_token()
        except Exception:
            resolved_token = None

    # 2. Store client per-session in Streamlit session_state if available
    try:
        import streamlit as st

        if "_api_client" not in st.session_state or st.session_state["_api_client"] is None:
            st.session_state["_api_client"] = ResearchAPIClient(token=resolved_token)

        client: ResearchAPIClient = st.session_state["_api_client"]
        if resolved_token is not None:
            client.set_token(resolved_token)
        return client
    except Exception:
        # Fallback for non-Streamlit environments (e.g. unit tests, CLI scripts)
        return ResearchAPIClient(token=resolved_token)
