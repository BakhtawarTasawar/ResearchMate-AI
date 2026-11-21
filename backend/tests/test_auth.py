"""
Authentication and JWT integration tests.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_auth_me_unauthorized():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert "Invalid or missing authentication token" in response.json()["detail"]


def test_auth_register_and_login_flow():
    import uuid
    uid = uuid.uuid4().hex[:8]
    email = f"researcher_{uid}@university.edu"
    password = "SecurePassword123!"

    # 1. Register
    reg_res = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Dr. Eleanor Vance",
            "email": email,
            "password": password,
        },
    )
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert reg_data["success"] is True
    assert reg_data["user"]["email"] == email

    # 2. Duplicate registration rejected
    dup_res = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Dr. Eleanor Vance",
            "email": email,
            "password": password,
        },
    )
    assert dup_res.status_code == 409

    # 3. Login with wrong password
    bad_login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "WrongPassword!"},
    )
    assert bad_login.status_code == 401

    # 4. Login successfully
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token

    # 5. Access /auth/me with Bearer token
    me_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email
