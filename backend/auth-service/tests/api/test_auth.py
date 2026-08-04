import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "StrongPassword#2026",
        "phone": "+919876543210"
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "testuser@example.com"
    assert data["data"]["role"] == "CITIZEN"
    assert "meta" in data
    assert "traceId" in data["meta"]


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    payload = {
        "full_name": "Weak User",
        "email": "weak@example.com",
        "password": "123",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "TSX-AUTH-009"
    assert "meta" in data


@pytest.mark.asyncio
async def test_login_and_refresh_flow(client: AsyncClient):
    # 1. Register
    reg_payload = {
        "full_name": "Flow User",
        "email": "flow@example.com",
        "password": "FlowPassword#2026"
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201

    # 2. Login
    login_payload = {
        "email": "flow@example.com",
        "password": "FlowPassword#2026"
    }
    login_res = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert login_data["success"] is True
    access_token = login_data["data"]["access_token"]
    assert access_token is not None

    # Verify Security Headers
    assert login_res.headers.get("X-Content-Type-Options") == "nosniff"
    assert login_res.headers.get("X-Frame-Options") == "DENY"
    assert login_res.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    # Verify HttpOnly Cookie was set
    assert "tsx_refresh_token" in login_res.cookies
    refresh_cookie = login_res.cookies["tsx_refresh_token"]

    # 3. Access Protected Route
    me_res = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["data"]["email"] == "flow@example.com"

    # 4. Refresh Token Rotation
    client.cookies.set("tsx_refresh_token", refresh_cookie)
    ref_res = await client.post("/api/v1/auth/refresh")
    assert ref_res.status_code == 200
    ref_data = ref_res.json()
    assert ref_data["success"] is True
    new_access_token = ref_data["data"]["access_token"]
    assert new_access_token != access_token

    # 5. Logout
    logout_res = await client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    assert logout_res.status_code == 200
    assert logout_res.json()["data"]["logged_out"] is True


@pytest.mark.asyncio
async def test_email_verification_flow(client: AsyncClient):
    resend_res = await client.post("/api/v1/auth/resend-verification", json={"email": "nonexistent@example.com"})
    assert resend_res.status_code == 200
    assert resend_res.json()["success"] is True

    invalid_v_res = await client.post("/api/v1/auth/verify-email", json={"token": "invalid_token_sample"})
    assert invalid_v_res.status_code == 400
    assert invalid_v_res.json()["success"] is False
    assert invalid_v_res.json()["error_code"] == "TSX-AUTH-008" or "TSX-AUTH-" in invalid_v_res.json()["error_code"]
