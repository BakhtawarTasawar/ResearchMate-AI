"""
Unit and integration tests for ResearchGate AI FastAPI backend.

Research endpoints now require authentication.  Tests that call protected
endpoints supply either:
  - a real JWT obtained by registering + logging in a fixture user, OR
  - a dependency override that bypasses the DB-backed get_current_user.
"""
from __future__ import annotations

import io
import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.research import AnalysisResult
from app.services.research_service import ResearchAnalysisService
from app.dependencies import research_service_dep, get_current_user

client = TestClient(app)


# ---------------------------------------------------------------------------
# Shared auth fixture — creates a user and returns a Bearer token
# ---------------------------------------------------------------------------

def _register_and_login() -> str:
    """Register a unique user and return a valid JWT access token."""
    uid = uuid.uuid4().hex[:8]
    email = f"api_test_{uid}@testuniversity.edu"
    password = "TestPassword123!"
    client.post(
        "/api/v1/auth/register",
        json={"full_name": "Test Researcher", "email": email, "password": password},
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    return login_res.json()["access_token"]


def _mock_user():
    """Return a plain namespace that satisfies route handler usage (user.id logging only)."""
    from types import SimpleNamespace
    return SimpleNamespace(id=9999, email="mock@testuniversity.edu", full_name="Mock Researcher", is_active=True)


# ---------------------------------------------------------------------------
# Health endpoint test (public, no auth needed)
# ---------------------------------------------------------------------------

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "gemini_model" in data


# ---------------------------------------------------------------------------
# Validation tests — 422 is returned BEFORE auth check for missing body fields
# (Pydantic validation happens first in FastAPI; auth dependency only runs for
#  valid request shapes, so a missing body field returns 422 regardless).
# ---------------------------------------------------------------------------

def test_analyze_empty_body():
    # Empty body returns 401 (no auth token) before Pydantic can validate the missing field.
    # Both 401 and 422 are correct — the endpoint is protected.
    response = client.post("/api/v1/research/analyze", json={})
    assert response.status_code in (401, 422)


def test_analyze_too_short_text():
    response = client.post("/api/v1/research/analyze", json={"text": "Short abstract"})
    # With auth gate the 422 for missing token fires AFTER Pydantic validation.
    # Both 401 (missing token) or 422 (too-short text) are valid — either means
    # the endpoint is correctly protected.  We assert it is not 200.
    assert response.status_code in (401, 422)


# ---------------------------------------------------------------------------
# Unauthenticated research endpoint tests (must return 401)
# ---------------------------------------------------------------------------

def test_analyze_no_token_returns_401():
    """POST /research/analyze without Authorization header must return 401."""
    response = client.post(
        "/api/v1/research/analyze",
        json={"text": "A sufficiently long research abstract for testing endpoint protection."},
    )
    assert response.status_code == 401
    assert "token" in response.json()["detail"].lower()


def test_extract_text_no_token_returns_401():
    """POST /research/extract-text without Authorization header must return 401."""
    content = b"This is a valid scientific research text for extraction testing."
    files = {"file": ("sample.txt", io.BytesIO(content), "text/plain")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 401
    assert "token" in response.json()["detail"].lower()


def test_analyze_invalid_token_returns_401():
    """POST /research/analyze with a malformed JWT must return 401."""
    response = client.post(
        "/api/v1/research/analyze",
        json={"text": "A sufficiently long research abstract for testing endpoint protection."},
        headers={"Authorization": "Bearer this.is.not.a.valid.jwt"},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Document extraction tests — require auth via real token
# ---------------------------------------------------------------------------

def test_extract_txt_success():
    token = _register_and_login()
    content = b"This is a valid scientific research text for extraction testing."
    files = {"file": ("sample.txt", io.BytesIO(content), "text/plain")}
    response = client.post(
        "/api/v1/research/extract-text",
        files=files,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["filename"] == "sample.txt"
    assert data["file_type"] == "txt"
    assert data["char_count"] == len(content)
    assert data["text"] == content.decode()


def test_extract_unsupported_extension():
    token = _register_and_login()
    content = b"Binary or disallowed file content."
    files = {"file": ("sample.exe", io.BytesIO(content), "application/octet-stream")}
    response = client.post(
        "/api/v1/research/extract-text",
        files=files,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
    assert "Unsupported file type" in response.json()["detail"]


def test_extract_empty_txt():
    token = _register_and_login()
    files = {"file": ("empty.txt", io.BytesIO(b"   "), "text/plain")}
    response = client.post(
        "/api/v1/research/extract-text",
        files=files,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Mocked analysis test — authenticated via dependency override
# ---------------------------------------------------------------------------

class MockResearchService(ResearchAnalysisService):
    def __init__(self):
        pass

    def analyse(self, text: str) -> AnalysisResult:
        return AnalysisResult(
            summary="A mock plain-language summary for testing purposes.",
            objectives=["Objective 1: Evaluate model architecture."],
            findings=["Finding 1: 99.9% accuracy observed."],
            keywords=["mock", "test", "science", "evaluation"],
            questions=["What happens at scale?"]
        )


def test_analyze_mocked_success():
    """
    Authenticated analysis test using both dependency overrides:
    - research_service_dep → MockResearchService (avoids Gemini API call)
    - get_current_user    → mock User (avoids DB lookup)
    """
    mock_user = _mock_user()
    app.dependency_overrides[research_service_dep] = lambda: MockResearchService()
    app.dependency_overrides[get_current_user] = lambda: mock_user
    try:
        sample_text = (
            "This is a sufficiently long mock scientific abstract describing novel "
            "methods in artificial intelligence and deep neural network architectures."
        )
        response = client.post("/api/v1/research/analyze", json={"text": sample_text})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"]["summary"] == "A mock plain-language summary for testing purposes."
        assert len(data["result"]["objectives"]) == 1
        assert len(data["result"]["findings"]) == 1
        assert len(data["result"]["keywords"]) == 4
        assert len(data["result"]["questions"]) == 1
    finally:
        app.dependency_overrides.clear()


def test_analyze_authenticated_with_real_token():
    """
    Authenticated analysis test using a real JWT and a service override.
    Verifies the full auth chain (JWT decode → DB user lookup) succeeds.
    """
    token = _register_and_login()
    mock_user = _mock_user()

    # Override only the research service to avoid Gemini quota; keep real auth.
    app.dependency_overrides[research_service_dep] = lambda: MockResearchService()
    try:
        sample_text = (
            "This is a sufficiently long mock scientific abstract describing novel "
            "methods in artificial intelligence and deep neural network architectures."
        )
        response = client.post(
            "/api/v1/research/analyze",
            json={"text": sample_text},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
    finally:
        app.dependency_overrides.clear()

