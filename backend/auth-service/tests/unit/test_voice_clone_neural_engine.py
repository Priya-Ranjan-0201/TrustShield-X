"""Unit tests for Phase 3.6 Part 2A-1 — AI Voice Clone Neural Inference Engine & Model Adapter Framework.

Tests cover:
- Model Adapter Framework (ECAPA-TDNN, SpeechBrain, WavLM, Resemblyzer, NeMo adapters)
- Extended Audio Model Registry (Model registration, metadata tracking, active adapter switching)
- Speaker Similarity Engine (Cosine Similarity, Euclidean Distance, Angular Distance metrics)
- Multi-Speaker Neural Inference & Conversation Risk Aggregation
- Confidence Calibration & False Positive Protection (LOW_CONFIDENCE trigger)
- Explainability Interface & Platform Evidence Generation
- Master AudioProcessingOrchestrator execution
"""

import pytest
from app.services.voice_model_adapter import (
    ECAPATDNNVoiceCloneAdapter,
    SpeechBrainVoiceCloneAdapter,
    WavLMVoiceCloneAdapter,
    ResemblyzerVoiceCloneAdapter,
    NeMoSpeakerNetVoiceCloneAdapter,
)
from app.services.audio_model_registry import AudioModelRegistry
from app.services.speaker_similarity_engine import (
    compute_cosine_similarity,
    compute_euclidean_distance,
    compute_angular_distance,
    analyze_speaker_embedding_similarity,
)
from app.services.voice_clone_analyzer import analyze_voice_clone_multi_speaker
from app.services.voice_calibrator import calibrate_voice_confidence
from app.services.voice_explainability import generate_voice_explainability
from app.services.audio_detector import AudioProcessingOrchestrator


# ============================================================
# 1. Model Adapter Framework Tests
# ============================================================

def test_ecapa_tdnn_model_adapter_lifecycle():
    adapter = ECAPATDNNVoiceCloneAdapter()
    assert adapter.model_name == "ECAPA-TDNN-VoiceClone"
    assert adapter.embedding_dim == 192
    assert adapter.initialize() is True
    assert adapter.load_weights() is True

    prep = adapter.preprocess(b"audio bytes", {"duration_sec": 10.0, "sample_rate": 44100})
    inf_out = adapter.infer(prep)

    assert inf_out.model_name == "ECAPA-TDNN-VoiceClone"
    assert isinstance(inf_out.raw_clone_score, float)
    assert inf_out.device_used in ("cpu", "cuda:0")

    post = adapter.postprocess(inf_out)
    assert "clone_probability" in post

    exp = adapter.explain(inf_out)
    assert exp["explanation_status"] == "EXPLAINABILITY_READY"
    assert adapter.unload() is True


def test_additional_model_adapters():
    adapters = [
        SpeechBrainVoiceCloneAdapter(),
        WavLMVoiceCloneAdapter(),
        ResemblyzerVoiceCloneAdapter(),
        NeMoSpeakerNetVoiceCloneAdapter(),
    ]
    for ad in adapters:
        assert ad.initialize() is True
        prep = ad.preprocess(b"audio bytes", {})
        inf_out = ad.infer(prep)
        assert inf_out.raw_clone_score >= 0.0
        assert ad.unload() is True


# ============================================================
# 2. Extended Audio Model Registry Tests
# ============================================================

def test_extended_audio_model_registry():
    registry = AudioModelRegistry()
    models = registry.list_registered_models()

    assert len(models) >= 9  # 4 embedding extractors + 5 voice clone classifiers

    active_adapter = registry.get_active_voice_adapter()
    assert active_adapter.model_name == "ECAPA-TDNN-VoiceClone"

    switched = registry.set_active_voice_adapter("WavLM-Large-VoiceClone")
    assert switched is True
    assert registry.get_active_voice_adapter().model_name == "WavLM-Large-VoiceClone"


# ============================================================
# 3. Speaker Similarity Engine Tests
# ============================================================

def test_speaker_similarity_metrics():
    vec_a = [1.0, 0.0, 0.0]
    vec_b = [1.0, 0.0, 0.0]
    vec_c = [0.0, 1.0, 0.0]

    assert compute_cosine_similarity(vec_a, vec_b) == 1.0
    assert compute_cosine_similarity(vec_a, vec_c) == 0.0

    assert compute_euclidean_distance(vec_a, vec_b) == 0.0
    assert compute_euclidean_distance(vec_a, vec_c) > 0.0

    assert compute_angular_distance(vec_a, vec_b) == 0.0

    embeddings = [
        {"speaker_id": "speaker_1", "embedding_vector": vec_a},
        {"speaker_id": "speaker_2", "embedding_vector": vec_b},
    ]

    analysis = analyze_speaker_embedding_similarity(embeddings)
    assert analysis["avg_cosine_similarity"] == 1.0
    assert analysis["similarity_anomaly_detected"] is True


# ============================================================
# 4. Multi-Speaker Neural Analysis Tests
# ============================================================

def test_analyze_voice_clone_multi_speaker():
    adapter = ECAPATDNNVoiceCloneAdapter()
    adapter.initialize()

    tracks = [
        {"speaker_id": "speaker_1", "total_speaking_duration": 5.0, "segment_count": 2},
        {"speaker_id": "speaker_2", "total_speaking_duration": 4.0, "segment_count": 1},
    ]

    res = analyze_voice_clone_multi_speaker(b"audio bytes", {"duration_sec": 10.0}, tracks, adapter)

    assert "overall_clone_probability" in res
    assert "highest_risk_speaker" in res
    assert len(res["per_speaker_results"]) == 2


# ============================================================
# 5. Confidence Calibration & False Positive Protection Tests
# ============================================================

def test_calibrate_voice_confidence():
    # Normal clear audio
    conf_high, state_high, _ = calibrate_voice_confidence(0.85, {"snr_db": 28.0, "clipping_ratio_percent": 0.0}, 5.0)
    assert conf_high >= 0.80
    assert state_high == "CALIBRATED_HIGH"

    # Short speech audio -> triggers LOW_CONFIDENCE
    conf_low, state_low, _ = calibrate_voice_confidence(0.85, {"snr_db": 28.0}, 0.8)
    assert state_low == "LOW_CONFIDENCE"


# ============================================================
# 6. Explainability & Evidence Generation Tests
# ============================================================

def test_generate_voice_explainability():
    clone_res = {
        "overall_clone_probability": 0.88,
        "highest_risk_speaker": "speaker_1",
        "highest_speaker_clone_prob": 0.88,
    }
    sim_res = {"similarity_anomaly_detected": True, "avg_cosine_similarity": 0.98}

    exp_dict, evidence = generate_voice_explainability(
        clone_res, sim_res, {"clipping_ratio_percent": 3.5}, "ECAPA-TDNN-VoiceClone", "CALIBRATED_HIGH"
    )

    assert exp_dict["spectrogram_readiness"] is True
    assert len(evidence) >= 2
    types = [e["type"] for e in evidence]
    assert "VOICE_CLONE" in types
    assert "SPEAKER_SIMILARITY_ANOMALY" in types


# ============================================================
# 7. Master Orchestrator End-to-End Test
# ============================================================

@pytest.mark.asyncio
async def test_audio_orchestrator_neural_pipeline():
    orchestrator = AudioProcessingOrchestrator()
    sample_wav = b"RIFF" + b"\x00" * 1000

    res = await orchestrator.analyze_audio(sample_wav, "sample.wav", "audio/wav")

    assert res.module == "audio-voice-ai"
    assert res.status == "completed"
    assert res.pipeline_status == "AI_CONVERSATION_INTELLIGENCE_COMPLETED"
    assert isinstance(res.risk_score, int)
    assert isinstance(res.confidence_score, float)
    assert len(res.evidence) >= 1
