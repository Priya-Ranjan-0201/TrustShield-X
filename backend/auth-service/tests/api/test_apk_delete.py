"""API tests for APK Scan Delete Endpoint (Phase 3.7 Part 1A Message 3C.1)."""

import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_delete_apk_unauthenticated(client: AsyncClient):
    fake_id = uuid.uuid4()
    res = await client.delete(f"/api/v1/apk/{fake_id}")
    assert res.status_code == 401
