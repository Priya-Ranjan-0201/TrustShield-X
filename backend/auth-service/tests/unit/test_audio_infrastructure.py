"""Unit tests for Phase 3.6 Part 1 — AI Voice Clone & Audio Scam Detection Infrastructure.

Tests cover:
- Audio validation (MIME, extension, size, corruption TSX-AUDIO-001, specification TSX-AUDIO-002)
- Technical metadata extraction (Sample rate, Duration, Channels, Bit depth, Codec, LUFS)
- Audio quality analysis (SNR dB, Clipping %, Silence %, Dynamic range)
- Voice Activity Detection (VAD speech vs silence timestamps)
- Intelligent audio segmentation strategies (Fixed, Adaptive, Speech, Silence boundary)
- Speaker diarization abstraction & timeline tracking
- Speaker embedding interface & Audio model registry (ECAPA-TDNN 192-dim)
- Master AudioProcessingOrchestrator pipeline execution
"""

import pytest
from app.services.audio_validator import validate_audio_file
from app.services.audio_metadata_extractor import extract_audio_metadata
from app.services.audio_quality_analyzer import analyze_audio_quality
from app.services.voice_activity_detector import detect_voice_activity
from app.services.audio_segmenter import segment_audio_intelligently
from app.services.speaker_diarizer import PyannoteSpeakerDiarizer
from app.services.speaker_tracker import track_speakers_across_timeline
from app.services.speaker_embedding_interface import ECAPATDNNEmbeddingExtractor
from app.services.audio_model_registry import AudioModelRegistry
from app.services.audio_detector import AudioProcessingOrchestrator


# ============================================================
# 1. Audio Validation Tests
# ============================================================

def test_validate_audio_file_valid_wav():
    wav_bytes = b"RIFF" + b"\x00" * 100
    res = validate_audio_file(wav_bytes, "sample.wav", "audio/wav")
    assert res.is_valid is True
    assert res.extension == ".wav"


def test_validate_audio_file_valid_mp3():
    mp3_bytes = b"ID3" + b"\x00" * 100
    res = validate_audio_file(mp3_bytes, "voice.mp3", "audio/mp3")
    assert res.is_valid is True
    assert res.extension == ".mp3"


def test_validate_audio_file_empty():
    res = validate_audio_file(b"", "empty.wav")
    assert res.is_valid is False
    assert res.error_code == "TSX-AUDIO-001"


def test_validate_audio_file_unsupported_ext():
    padded_bytes = b"RIFF" + b"\x00" * 100
    res = validate_audio_file(padded_bytes, "file.xyz", "application/xyz")
    assert res.is_valid is False
    assert res.error_code == "TSX-AUDIO-002"


# ============================================================
# 2. Metadata Extraction Tests
# ============================================================

def test_extract_audio_metadata():
    sample_bytes = b"RIFF" + b"\x00" * 500
    meta = extract_audio_metadata(sample_bytes, ".wav")
    assert meta.duration_sec >= 0.1
    assert meta.sample_rate >= 8000
    assert meta.channels in (1, 2)
    assert meta.codec == "WAV"


# ============================================================
# 3. Quality Analysis Tests
# ============================================================

def test_analyze_audio_quality():
    sample_bytes = bytes(range(256)) * 50
    quality = analyze_audio_quality(sample_bytes, 10.0, 44100)

    assert "overall_quality_score" in quality
    assert "snr_db" in quality
    assert "clipping_ratio_percent" in quality
    assert "silence_ratio_percent" in quality
    assert quality["overall_quality_score"] >= 0


# ============================================================
# 4. Voice Activity Detection & Segmentation Tests
# ============================================================

def test_voice_activity_detection():
    vad_segs = detect_voice_activity(b"audio bytes", duration_sec=10.0)
    assert len(vad_segs) >= 1
    assert any(s.is_speech for s in vad_segs)
    assert vad_segs[0].start_time_sec >= 0.0


def test_audio_segmenter_strategies():
    vad_segs = detect_voice_activity(b"audio bytes", duration_sec=10.0)

    fixed_chunks = segment_audio_intelligently(vad_segs, 10.0, strategy="FIXED_WINDOW", target_window_sec=3.0)
    assert len(fixed_chunks) >= 3

    boundary_chunks = segment_audio_intelligently(vad_segs, 10.0, strategy="SPEECH_BOUNDARY")
    assert len(boundary_chunks) >= 1


# ============================================================
# 5. Speaker Diarization & Tracking Tests
# ============================================================

def test_speaker_diarizer_and_tracker():
    vad_segs = detect_voice_activity(b"audio bytes", duration_sec=10.0)
    diarizer = PyannoteSpeakerDiarizer()
    diarized = diarizer.diarize_audio(b"audio bytes", vad_segs)

    assert len(diarized) >= 1

    tracks = track_speakers_across_timeline(diarized)
    assert len(tracks) >= 1
    assert tracks[0].total_speaking_duration > 0.0


# ============================================================
# 6. Speaker Embedding Interface & Model Registry Tests
# ============================================================

def test_speaker_embedding_interface():
    extractor = ECAPATDNNEmbeddingExtractor()
    assert extractor.extractor_name == "ECAPA-TDNN"
    assert extractor.embedding_dim == 192
    assert extractor.initialize() is True

    prep = extractor.preprocess(b"audio bytes")
    out = extractor.extract_embedding(prep, speaker_id="speaker_1")

    assert out.embedding_dim == 192
    assert len(out.embedding_vector) == 192
    assert extractor.unload() is True


def test_audio_model_registry():
    registry = AudioModelRegistry()
    models = registry.list_registered_models()
    assert len(models) >= 4

    active = registry.get_active_extractor()
    assert active.extractor_name == "ECAPA-TDNN"

    switched = registry.set_active_model("Resemblyzer-d-vector")
    assert switched is True
    assert registry.get_active_extractor().extractor_name == "Resemblyzer-d-vector"


# ============================================================
# 7. Master Audio Orchestrator Integration Test
# ============================================================

@pytest.mark.asyncio
async def test_audio_orchestrator_pipeline():
    orchestrator = AudioProcessingOrchestrator()
    sample_wav = b"RIFF" + b"\x00" * 1000

    res = await orchestrator.analyze_audio(sample_wav, "sample.wav", "audio/wav")

    assert res.module == "audio-voice-ai"
    assert res.status == "completed"
    assert res.pipeline_status == "AI_CONVERSATION_INTELLIGENCE_COMPLETED"
    assert len(res.speech_segments) >= 1
    assert len(res.speaker_tracks) >= 1
    assert len(res.speaker_embeddings_summary) >= 1
    assert res.execution_time_ms >= 0
