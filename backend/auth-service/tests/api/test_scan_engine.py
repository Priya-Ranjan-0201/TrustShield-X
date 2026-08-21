import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_create_and_execute_scan_flow(client: AsyncClient):
    # 1. Register user
    reg_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "scanuser@truthshield.gov.in",
            "password": "SecurePassword123!",
            "full_name": "Scan Engine Tester",
        },
    )
    assert reg_res.status_code == status.HTTP_201_CREATED

    # 2. Login user to retrieve access token
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "scanuser@truthshield.gov.in", "password": "SecurePassword123!"},
    )
    assert login_res.status_code == status.HTTP_200_OK
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Submit URL scan to POST /api/v1/scan
    scan_res = await client.post(
        "/api/v1/scan",
        data={"scan_type": "URL", "target_input": "https://trusted-bank-verification.in"},
        headers=headers,
    )
    assert scan_res.status_code == status.HTTP_200_OK
    scan_data = scan_res.json()["data"]
    assert scan_data["status"] == "COMPLETED"
    scan_id = scan_data["id"]

    # 4. Fetch scan events via GET /api/v1/scan/events/{scanId}
    events_res = await client.get(f"/api/v1/scan/events/{scan_id}", headers=headers)
    assert events_res.status_code == status.HTTP_200_OK
    events = events_res.json()["data"]
    assert len(events) >= 4  # SCAN_CREATED, SCAN_VALIDATED, SCAN_QUEUED, SCAN_STARTED, SCAN_COMPLETED

    # 5. Fetch scan details via GET /api/v1/scan/{scanId}
    details_res = await client.get(f"/api/v1/scan/{scan_id}", headers=headers)
    assert details_res.status_code == status.HTTP_200_OK
    assert details_res.json()["data"]["id"] == scan_id

    # 6. Delete scan via DELETE /api/v1/scan/{scan_id}
    del_res = await client.delete(f"/api/v1/scan/{scan_id}", headers=headers)
    assert del_res.status_code == status.HTTP_200_OK
    assert del_res.json()["data"]["deleted"] is True
