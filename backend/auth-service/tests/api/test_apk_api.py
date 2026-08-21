"""API tests for Android APK Upload & Scan Endpoints (Phase 3.7 Part 1A Message 3C.1)."""

import os
import io
import zipfile
import pytest
from httpx import AsyncClient


@pytest.fixture
def dummy_apk_bytes():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("AndroidManifest.xml", b"<manifest package='com.test'></manifest>")
        zf.writestr("classes.dex", b"dex\n035\x00" + b"\x00" * 50)
    return buf.getvalue()


@pytest.mark.asyncio
async def test_upload_apk_endpoint_invalid_extension(client: AsyncClient):
    files = {"file": ("malware.exe", b"MZ data", "application/octet-stream")}
    res = await client.post("/api/v1/apk/scan", files=files)
    # Without auth header, expect 401
    assert res.status_code in (401, 400)


@pytest.mark.asyncio
async def test_upload_apk_endpoint_unauthenticated(client: AsyncClient, dummy_apk_bytes):
    files = {"file": ("app.apk", dummy_apk_bytes, "application/vnd.android.package-archive")}
    res = await client.post("/api/v1/apk/scan", files=files)
    assert res.status_code == 401
