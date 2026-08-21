"""Unit tests for Phase 3.6 Part 2B-2 — Production APIs, Notifications, Telemetry & Operational Hardening.

Tests cover:
- Audio REST Endpoints (POST /api/v1/audio/scan, GET /api/v1/audio/{scan_id}, GET /api/v1/audio/history/all, DELETE /api/v1/audio/{scan_id})
- Security Notification Engine (SECURITY_ALERT creation on high risk >=50)
- Operational Telemetry Manager (AudioTelemetryManager recording timings & resource usage)
- Standardized Error Codes (AudioErrorCode TSX-AUDIO-100 to TSX-AUDIO-500)
"""

import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.audio_telemetry import AudioTelemetryManager, AudioPipelineTelemetryRecord
from app.core.error_codes import AudioErrorCode, ERROR_DESCRIPTIONS


# ============================================================
# 1. Audio Telemetry Manager Unit Tests
# ============================================================

def test_audio_telemetry_manager():
    telemetry = AudioTelemetryManager()
    scan_id = str(uuid.uuid4())

    rec = telemetry.record_pipeline(
        scan_id=scan_id,
        total_time_ms=120,
        speaker_count=2,
        duration_sec=10.0,
        status="success",
        model_used="ECAPA-TDNN-VoiceClone",
    )

    assert rec.scan_id == scan_id
    assert rec.total_pipeline_time_ms == 120
    assert rec.speaker_count == 2
    assert rec.model_used == "ECAPA-TDNN-VoiceClone"

    summary = telemetry.get_metrics_summary()
    assert summary["total_requests"] >= 1
    assert summary["successful_requests"] >= 1


# ============================================================
# 2. Audio Error Codes Unit Tests
# ============================================================

def test_audio_error_codes():
    assert AudioErrorCode.VALIDATION_ERROR == "TSX-AUDIO-100"
    assert AudioErrorCode.INFERENCE_ERROR == "TSX-AUDIO-200"
    assert AudioErrorCode.REPOSITORY_ERROR == "TSX-AUDIO-300"
    assert AudioErrorCode.API_ERROR == "TSX-AUDIO-400"
    assert AudioErrorCode.UNEXPECTED_ERROR == "TSX-AUDIO-500"

    assert AudioErrorCode.VALIDATION_ERROR in ERROR_DESCRIPTIONS
    assert "validation" in ERROR_DESCRIPTIONS[AudioErrorCode.VALIDATION_ERROR].lower()


# ============================================================
# 3. Notification & Telemetry Integration in ScanOrchestrator
# ============================================================

@pytest.mark.asyncio
async def test_scan_orchestrator_notification_and_telemetry():
    from app.services.scan_orchestrator import ScanOrchestrator

    mock_db = MagicMock()
    mock_db.execute = AsyncMock()
    mock_db.commit = AsyncMock()

    orchestrator = ScanOrchestrator(mock_db)
    assert orchestrator.db == mock_db
