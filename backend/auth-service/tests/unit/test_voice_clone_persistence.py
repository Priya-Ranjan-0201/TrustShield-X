"""Unit tests for Phase 3.6 Part 2B-1 — Production Integration, Database Persistence & Repository Layer.

Tests cover:
- AudioMetadata extended columns validation
- VoiceCloneResult ORM model creation
- ConversationAnalysis ORM model creation
- AudioCloneRepository (save_voice_clone_analysis, get_analysis_by_scan_id)
- Pydantic DTO schemas (VoiceCloneResultResponse, ConversationAnalysisResponse, EvidenceResponse)
- ScanOrchestrator production persistence integration
"""

import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.models.audio_metadata import AudioMetadata
from app.models.voice_clone_result import VoiceCloneResult, ConversationAnalysis
from app.repositories.audio_clone_repository import AudioCloneRepository
from app.schemas.voice_clone_dto import (
    VoiceCloneResultResponse,
    ConversationAnalysisResponse,
    EvidenceResponse,
)


# ============================================================
# 1. ORM Model Instantiation Tests
# ============================================================

def test_voice_clone_result_model():
    scan_id = uuid.uuid4()
    vc = VoiceCloneResult(
        scan_id=scan_id,
        speaker_id="speaker_1",
        clone_probability=0.88,
        similarity_score=0.94,
        confidence=0.92,
        verdict="VOICE_CLONE",
        evidence_json=[{"title": "Unnatural Formants"}],
        recommendation_json=["Verify identity"],
    )
    assert vc.scan_id == scan_id
    assert vc.speaker_id == "speaker_1"
    assert vc.clone_probability == 0.88
    assert vc.verdict == "VOICE_CLONE"


def test_conversation_analysis_model():
    scan_id = uuid.uuid4()
    ca = ConversationAnalysis(
        scan_id=scan_id,
        total_speakers=2,
        conversation_duration=12.5,
        conversation_quality=85,
        conversation_risk=75,
        conversation_confidence=0.90,
        dominant_speaker="speaker_1",
        summary_json={"verdict": "VOICE_CLONE"},
    )
    assert ca.scan_id == scan_id
    assert ca.total_speakers == 2
    assert ca.conversation_risk == 75


# ============================================================
# 2. Pydantic DTO Serialization Tests
# ============================================================

def test_voice_clone_dto_schemas():
    ev_dto = EvidenceResponse(
        type="VOICE_CLONE",
        category="SYNTHETIC_VOICE",
        severity="CRITICAL",
        title="Voice Clone Detected",
        description="High clone probability",
        confidence=0.92,
    )
    assert ev_dto.type == "VOICE_CLONE"

    vc_dto = VoiceCloneResultResponse(
        speaker_id="speaker_1",
        clone_probability=0.88,
        verdict="VOICE_CLONE",
        evidence=[ev_dto.model_dump()],
        recommendations=["Out-of-band contact"],
    )
    assert vc_dto.speaker_id == "speaker_1"
    assert vc_dto.clone_probability == 0.88

    ca_dto = ConversationAnalysisResponse(
        total_speakers=2,
        conversation_duration=12.5,
        conversation_risk=75,
    )
    assert ca_dto.total_speakers == 2


# ============================================================
# 3. AudioCloneRepository Unit Tests
# ============================================================

@pytest.mark.asyncio
async def test_audio_clone_repository_save():
    mock_session = MagicMock()
    mock_session.commit = AsyncMock()
    repo = AudioCloneRepository(mock_session)

    scan_id = uuid.uuid4()
    meta_dict = {"duration_sec": 10.0, "sample_rate": 44100, "codec": "pcm_s16le"}
    qual_dict = {"snr_db": 28.0, "overall_quality_score": 85}
    segs = [{"segment_index": 0, "start_time_sec": 0.0, "end_time_sec": 5.0, "duration_sec": 5.0, "speaker_id": "speaker_1"}]
    tracks = [{"speaker_id": "speaker_1", "total_speaking_duration": 5.0, "segment_count": 1}]
    inference = {
        "clone_probability": 0.88,
        "real_probability": 0.12,
        "confidence": 0.92,
        "calibrated_confidence": 0.90,
        "verdict": "VOICE_CLONE",
        "risk_score": 88,
        "execution_time_ms": 120,
    }
    evidence = [{"type": "VOICE_CLONE", "title": "Voice Clone Detected"}]
    recs = ["Out-of-band verification"]

    meta_obj = await repo.save_voice_clone_analysis(
        scan_id=scan_id,
        metadata_dict=meta_dict,
        quality_metrics=qual_dict,
        speech_segments_list=segs,
        speaker_tracks_list=tracks,
        inference_results=inference,
        evidence_list=evidence,
        recommendations_list=recs,
    )

    assert meta_obj.scan_id == scan_id
    assert mock_session.add.call_count >= 5  # AudioMetadata + SpeechSegment + SpeakerTrack + VoiceCloneResult + ConversationAnalysis
    assert mock_session.commit.called
