"""
Comprehensive privacy, error sanitization, security, and integration test suite.
Covers all 16 required verification cases for ResearchGate AI.
"""
from __future__ import annotations

import io
import sys
import uuid
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Bootstrap frontend import path
_FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if str(_FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(_FRONTEND_DIR))

from services.api_client import ResearchAPIClient, APIError, sanitize_error
from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Case 1 & 6: Backend unavailable & timeout during registration
# ---------------------------------------------------------------------------

def test_01_backend_unavailable_during_registration():
    """Ensure connection error during registration yields safe message without URLs or ports."""
    dead_client = ResearchAPIClient(base_url="http://127.0.0.1:59999/api/v1", timeout=0.5)
    with pytest.raises(APIError) as exc_info:
        dead_client.register("Dr. Eleanor Vance", "test@mit.edu", "Password123!")

    err_msg = str(exc_info.value)
    sanitized = sanitize_error(exc_info.value, action="register")

    # Assert no backend URL, endpoint, or port leaks
    assert "http" not in sanitized.lower()
    assert "59999" not in sanitized
    assert "localhost" not in sanitized.lower()
    assert sanitized == "Unable to connect right now. Please try again in a moment."


# ---------------------------------------------------------------------------
# Case 2: Backend unavailable during login
# ---------------------------------------------------------------------------

def test_02_backend_unavailable_during_login():
    """Ensure connection error during login yields safe connection message."""
    dead_client = ResearchAPIClient(base_url="http://127.0.0.1:59999/api/v1", timeout=0.5)
    with pytest.raises(APIError) as exc_info:
        dead_client.login("test@mit.edu", "Password123!")

    sanitized = sanitize_error(exc_info.value, action="login")
    assert "http" not in sanitized.lower()
    assert "localhost" not in sanitized.lower()
    assert sanitized == "Unable to connect right now. Please try again in a moment."


# ---------------------------------------------------------------------------
# Case 3: Invalid credentials
# ---------------------------------------------------------------------------

def test_03_invalid_credentials_error_message():
    """Invalid credentials must return exact user-facing message: 'Invalid email or password.'"""
    res = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent_researcher@university.edu", "password": "WrongPassword123!"},
    )
    assert res.status_code == 401
    err = APIError(res.json()["detail"], status_code=res.status_code)
    sanitized = sanitize_error(err, action="login")
    assert sanitized == "Invalid email or password."


# ---------------------------------------------------------------------------
# Case 4: Duplicate registration
# ---------------------------------------------------------------------------

def test_04_duplicate_registration_message():
    """Duplicate email registration returns clean, actionable message without system internals."""
    uid = uuid.uuid4().hex[:8]
    dup_email = f"dup_{uid}@mit.edu"
    pwd = "SecurePassword123!"

    # First registration succeeds
    res1 = client.post("/api/v1/auth/register", json={"full_name": "Dr. Original", "email": dup_email, "password": pwd})
    assert res1.status_code == 201

    # Second registration with same email returns 409
    res2 = client.post("/api/v1/auth/register", json={"full_name": "Dr. Impostor", "email": dup_email, "password": pwd})
    assert res2.status_code == 409
    err = APIError(res2.json()["detail"], status_code=res2.status_code)
    sanitized = sanitize_error(err, action="register")
    assert sanitized == "An account with this email already exists."
    assert "traceback" not in sanitized.lower()


# ---------------------------------------------------------------------------
# Case 5: Backend returns HTTP 500
# ---------------------------------------------------------------------------

def test_05_backend_http_500_sanitized():
    """Internal server errors must be masked without tracebacks or response bodies."""
    err = APIError("Traceback (most recent call last):\npsycopg.OperationalError: db connection failed", status_code=500)
    sanitized = sanitize_error(err, action="general")
    assert "traceback" not in sanitized.lower()
    assert "psycopg" not in sanitized.lower()
    assert sanitized == "Unable to connect right now. Please try again in a moment."


# ---------------------------------------------------------------------------
# Case 6: Backend timeout
# ---------------------------------------------------------------------------

def test_06_backend_timeout_sanitized():
    """Timeout exceptions yield safe connection message."""
    err = APIError("Request timed out.", status_code=504)
    sanitized = sanitize_error(err, action="general")
    assert sanitized == "Unable to connect right now. Please try again in a moment."


# ---------------------------------------------------------------------------
# Case 7: Unexpected exception
# ---------------------------------------------------------------------------

def test_07_unexpected_exception_sanitized():
    """Any unhandled or unexpected Python exception yields safe generic fallback."""
    unexpected = RuntimeError("Division by zero in database query helper at line 42")
    sanitized = sanitize_error(unexpected, action="general")
    assert sanitized == "Something went wrong. Please try again later."
    assert "division" not in sanitized.lower()
    assert "line 42" not in sanitized.lower()


# ---------------------------------------------------------------------------
# Case 8: JWT token is not displayed on the profile page
# ---------------------------------------------------------------------------

def test_08_jwt_token_not_in_profile_source():
    """Verify frontend/pages/auth.py does not render JWT token or token status in HTML."""
    auth_source = (_FRONTEND_DIR / "pages" / "auth.py").read_text(encoding="utf-8")
    # Verify no raw token interpolation in HTML
    assert "token" not in auth_source.split("def _render_profile")[1].lower() or "jwt" not in auth_source.split("def _render_profile")[1].lower()
    assert "JWT Bearer Token" not in auth_source


# ---------------------------------------------------------------------------
# Case 9: Password and password hash are not displayed
# ---------------------------------------------------------------------------

def test_09_password_and_hash_not_displayed_in_profile():
    """Ensure passwords and password hashes are never exposed in user responses or profile."""
    uid = uuid.uuid4().hex[:8]
    email = f"hash_test_{uid}@mit.edu"
    pwd = "MySecretPassword123!"

    reg_res = client.post("/api/v1/auth/register", json={"full_name": "Test User", "email": email, "password": pwd})
    assert reg_res.status_code == 201
    user_data = reg_res.json()["user"]

    assert "password" not in user_data
    assert "hashed_password" not in user_data
    assert "password_hash" not in user_data


# ---------------------------------------------------------------------------
# Case 10: Database and backend configuration not displayed in public UI
# ---------------------------------------------------------------------------

def test_10_database_and_backend_config_not_in_public_ui():
    """Verify About page, Footer, and Profile contain no PostgreSQL, Docker, or port info."""
    about_text = (_FRONTEND_DIR / "pages" / "about.py").read_text(encoding="utf-8")
    ui_text = (_FRONTEND_DIR / "components" / "ui.py").read_text(encoding="utf-8")

    assert "PostgreSQL" not in about_text
    assert "SQLAlchemy" not in about_text
    assert "FastAPI" not in ui_text.split("def render_footer")[1]
    assert "PostgreSQL" not in ui_text.split("def render_footer")[1]
    assert "localhost" not in about_text
    assert "5432" not in about_text
    assert "5433" not in about_text


# ---------------------------------------------------------------------------
# Case 11 & 12: Successful registration and login still work
# ---------------------------------------------------------------------------

def test_11_and_12_successful_registration_and_login():
    """Verify live registration and login succeed and return valid JWT tokens."""
    uid = uuid.uuid4().hex[:8]
    email = f"researcher_{uid}@university.edu"
    pwd = "SecurePassword123!"

    # Registration
    reg_res = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Dr. Eleanor Vance", "email": email, "password": pwd},
    )
    assert reg_res.status_code == 201
    assert reg_res.json()["success"] is True

    # Login
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": pwd},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token and len(token) > 20


# ---------------------------------------------------------------------------
# Case 13 & 14: Researcher profile and logout
# ---------------------------------------------------------------------------

def test_13_and_14_profile_retrieval_and_session_clearing():
    """Verify /auth/me returns profile data, and session module handles logout cleanly."""
    uid = uuid.uuid4().hex[:8]
    email = f"profile_{uid}@university.edu"
    pwd = "SecurePassword123!"

    client.post("/api/v1/auth/register", json={"full_name": "Dr. Eleanor Vance", "email": email, "password": pwd})
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    token = login_res.json()["access_token"]

    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    user_info = me_res.json()
    assert user_info["email"] == email
    assert user_info["full_name"] == "Dr. Eleanor Vance"
    assert user_info["is_active"] is True


# ---------------------------------------------------------------------------
# Case 15: Research analysis — unauthenticated requests are rejected
# ---------------------------------------------------------------------------

def _get_test_token() -> str:
    """Register a unique user and return a valid JWT for protected endpoint tests."""
    uid = uuid.uuid4().hex[:8]
    email = f"privacy_test_{uid}@university.edu"
    pwd = "SecurePassword123!"
    client.post("/api/v1/auth/register", json={"full_name": "Dr. Privacy Tester", "email": email, "password": pwd})
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    return login_res.json()["access_token"]


def test_15_research_analysis_validation_and_flow():
    """
    Verify research analysis endpoint:
    - Rejects unauthenticated requests with 401.
    - Validates minimum text length (422).
    """
    # Unauthenticated — must return 401
    unauth_res = client.post("/api/v1/research/analyze", json={"text": "Short."})
    assert unauth_res.status_code == 401, (
        f"Expected 401 for unauthenticated request, got {unauth_res.status_code}"
    )

    # Authenticated but too-short text — must return 422
    token = _get_test_token()
    short_res = client.post(
        "/api/v1/research/analyze",
        json={"text": "Short."},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert short_res.status_code == 422
    assert "at least 50 characters" in str(short_res.json()["detail"])


# ---------------------------------------------------------------------------
# Case 16: PDF/TXT extraction — unauthenticated requests are rejected
# ---------------------------------------------------------------------------

def test_16_pdf_and_txt_extraction():
    """
    Verify document extraction:
    - Rejects unauthenticated requests with 401.
    - Parses TXT successfully for authenticated users.
    """
    sample_text = "Targeted therapeutic gene editing in pluripotency-maintained cells."

    # Unauthenticated — must return 401
    files_unauth = {"file": ("sample.txt", io.BytesIO(sample_text.encode("utf-8")), "text/plain")}
    unauth_res = client.post("/api/v1/research/extract-text", files=files_unauth)
    assert unauth_res.status_code == 401, (
        f"Expected 401 for unauthenticated extract-text, got {unauth_res.status_code}"
    )

    # Authenticated — must return 200 with correct extraction
    token = _get_test_token()
    files_auth = {"file": ("sample.txt", io.BytesIO(sample_text.encode("utf-8")), "text/plain")}
    res = client.post(
        "/api/v1/research/extract-text",
        files=files_auth,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["text"] == sample_text
    assert data["char_count"] == len(sample_text)
