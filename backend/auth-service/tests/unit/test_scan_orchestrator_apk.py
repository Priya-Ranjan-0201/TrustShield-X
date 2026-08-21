"""Unit tests for ScanOrchestrator APK Dispatching (Phase 3.7 Part 1A Message 3B)."""

import uuid
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.scan_orchestrator import ScanOrchestrator, DefaultModuleRouter


def test_module_router_apk_resolution():
    router = DefaultModuleRouter()
    target_module = router.resolve_target_module("APK")
    assert target_module == "apk-malware-ai"


@pytest.mark.asyncio
async def test_scan_orchestrator_apk_dispatch():
    db_mock = AsyncMock()
    orchestrator = ScanOrchestrator(db_mock)
    scan_id = uuid.uuid4()

    from app.core.scan_lifecycle import ScanStatus
    mock_scan = MagicMock()
    mock_scan.id = scan_id
    mock_scan.user_id = uuid.uuid4()
    mock_scan.scan_type = "APK"
    mock_scan.status = ScanStatus.UPLOADED
    mock_scan.target = "test_app.apk"
    mock_scan.file_path = None
    mock_scan.mime_type = "application/vnd.android.package-archive"
    mock_scan.module_used = "apk-malware-ai"

    with patch("sqlalchemy.select") as mock_select:
        mock_exec_res = MagicMock()
        mock_exec_res.scalar_one_or_none.return_value = mock_scan
        db_mock.execute.return_value = mock_exec_res

        with patch("app.services.apk_processing_service.APKProcessingService.process_apk_file", new_callable=AsyncMock) as mock_apk_proc:
            mock_proc_res = MagicMock()
            mock_proc_res.parsed_successfully = True
            mock_proc_res.processing_time_ms = 150
            mock_proc_res.to_dict.return_value = {"parsed_successfully": True}
            mock_apk_proc.return_value = mock_proc_res

            res = await orchestrator.execute_pipeline(scan_id)
            assert res is True
            assert mock_apk_proc.called
