"""Unit tests for APK Processing Service (Phase 3.7 Part 1A Message 3B)."""

import os
import uuid
import zipfile
import tempfile
import pytest
from unittest.mock import AsyncMock, patch
from app.services.apk_processing_service import APKProcessingService


@pytest.fixture
def sample_apk_path():
    buf = tempfile.NamedTemporaryFile(delete=False, suffix=".apk")
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("AndroidManifest.xml", b"<manifest package='com.test.app'></manifest>")
        zf.writestr("classes.dex", b"dex\n035\x00" + b"\x00" * 100)
    buf.close()
    yield buf.name
    if os.path.exists(buf.name):
        os.remove(buf.name)


@pytest.mark.asyncio
async def test_apk_processing_service_flow(sample_apk_path):
    db_mock = AsyncMock()
    service = APKProcessingService(db_mock)
    scan_id = uuid.uuid4()

    with patch.object(service.apk_repo, "save_apk_analysis", new_callable=AsyncMock) as mock_save:
        mock_save.return_value = AsyncMock()

        res = await service.process_apk_file(
            scan_id=scan_id,
            file_path=sample_apk_path,
            filename="sample.apk",
        )

        assert res.parsed_successfully is True
        assert res.scan_id == str(scan_id)
        assert res.processing_time_ms >= 0
        assert mock_save.called
