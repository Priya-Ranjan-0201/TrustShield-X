"""API tests for User APK Scan History Endpoint (Phase 3.7 Part 1A Message 3C.1)."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_apk_history_unauthenticated(client: AsyncClient):
    res = await client.get("/api/v1/apk/history")
    assert res.status_code == 401
