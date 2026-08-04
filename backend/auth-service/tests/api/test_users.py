import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_profile_and_sessions(client: AsyncClient):
    # 1. Register User
    reg_res = await client.post("/api/v1/auth/register", json={
        "full_name": "Profile Session User",
        "email": "profilesession@example.com",
        "password": "ProfilePassword#2026",
    })
    assert reg_res.status_code == 201

    # 2. Login
    login_res = await client.post("/api/v1/auth/login", json={
        "email": "profilesession@example.com",
        "password": "ProfilePassword#2026",
    })
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get Active Sessions
    sessions_res = await client.get("/api/v1/users/sessions", headers=headers)
    assert sessions_res.status_code == 200
    sessions_data = sessions_res.json()
    assert sessions_data["success"] is True
    assert len(sessions_data["data"]) >= 1

    # 4. Update Profile
    update_res = await client.put("/api/v1/users/me", headers=headers, json={
        "full_name": "Updated Profile User",
        "phone": "+919999988888"
    })
    assert update_res.status_code == 200
    assert update_res.json()["data"]["full_name"] == "Updated Profile User"

    # 5. Change Password
    pw_change_res = await client.put("/api/v1/users/change-password", headers=headers, json={
        "current_password": "ProfilePassword#2026",
        "new_password": "NewProfilePassword#2026"
    })
    assert pw_change_res.status_code == 200
    assert pw_change_res.json()["data"]["password_changed"] is True

    # 6. Revoke All Sessions
    # Re-login with new password to get active token
    new_login_res = await client.post("/api/v1/auth/login", json={
        "email": "profilesession@example.com",
        "password": "NewProfilePassword#2026",
    })
    new_token = new_login_res.json()["data"]["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}

    revoke_all_res = await client.delete("/api/v1/users/sessions", headers=new_headers)
    assert revoke_all_res.status_code == 200
    assert revoke_all_res.json()["success"] is True
