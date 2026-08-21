"""Unit tests for Phase 3.5 Part 2A — AI Deepfake Neural Inference Engine & Model Adapter Framework.

Tests cover:
- Model Adapter Framework for 6 architectures (EfficientNet, MesoNet, XceptionNet, Swin, ViT, CLIP)
- Extended Model Registry with dynamic active model switching & device auto-detection
- Temporal Frame Aggregation strategies (AVERAGE, WEIGHTED_AVERAGE, MEDIAN, CONFIDENCE_WEIGHTED)
- Multi-Face Video Risk Aggregation & highest risk face tracking
- Confidence Calibration & False Positive Protection (LOW_CONFIDENCE)
- Neural Explainability Interface & Evidence Generation
- Master DeepfakePipelineOrchestrator neural inference pipeline
"""

import pytest
from app.services.deepfake_model_adapter import (
    EfficientNetDeepfakeAdapter,
    MesoNetDeepfakeAdapter,
    XceptionNetDeepfakeAdapter,
    SwinTransformerDeepfakeAdapter,
    ViTDeepfakeAdapter,
    CLIPDeepfakeAdapter,
    NeuralInferenceOutput,
)
from app.services.deepfake_model_registry import DeepfakeModelRegistryExtended
from app.services.deepfake_aggregator import (
    aggregate_temporal_predictions,
    aggregate_multi_face_predictions,
)
from app.services.deepfake_calibrator import calibrate_deepfake_confidence
from app.services.deepfake_explainability import (
    generate_deepfake_explainability,
    generate_deepfake_evidence_cards,
)
from app.services.deepfake_detector import DeepfakePipelineOrchestrator


# ============================================================
# 1. Model Adapter Framework Tests
# ============================================================

def test_efficientnet_adapter():
    adapter = EfficientNetDeepfakeAdapter()
    assert adapter.model_name == "EfficientNet-B0-Deepfake"
    assert adapter.architecture == "EfficientNet-B0"
    assert adapter.input_size == (224, 224)
    assert adapter.initialize() is True

    prep = adapter.preprocess([b"fake_chip_1", b"fake_chip_2"])
    assert prep["batch_size"] == 2

    out = adapter.infer(prep)
    assert isinstance(out, NeuralInferenceOutput)
    assert 0.0 <= out.fake_probability <= 1.0
    assert round(out.fake_probability + out.real_probability, 3) == 1.0
    assert adapter.unload() is True


def test_all_model_adapters():
    adapters = [
        MesoNetDeepfakeAdapter(),
        XceptionNetDeepfakeAdapter(),
        SwinTransformerDeepfakeAdapter(),
        ViTDeepfakeAdapter(),
        CLIPDeepfakeAdapter(),
    ]

    for adapter in adapters:
        assert adapter.initialize() is True
        prep = adapter.preprocess([b"chip_data"])
        out = adapter.infer(prep)
        assert out.fake_probability >= 0.0
        exp = adapter.explain(out)
        assert "explanation_type" in exp
        assert adapter.unload() is True


# ============================================================
# 2. Model Registry Extension Tests
# ============================================================

def test_extended_model_registry():
    registry = DeepfakeModelRegistryExtended()
    models = registry.list_registered_models()
    assert len(models) >= 6

    # EfficientNet is active default
    active = registry.get_active_adapter()
    assert active.model_name == "EfficientNet-B0-Deepfake"

    # Switch to XceptionNet
    switched = registry.set_active_model("XceptionNet-FF++")
    assert switched is True
    assert registry.get_active_adapter().model_name == "XceptionNet-FF++"


# ============================================================
# 3. Temporal & Multi-Face Aggregation Tests
# ============================================================

def test_temporal_aggregation_strategies():
    probs = [0.1, 0.8, 0.9, 0.4]
    confs = [0.9, 0.95, 0.92, 0.88]

    avg_prob = aggregate_temporal_predictions(probs, confs, "AVERAGE")
    assert avg_prob == pytest.approx(0.55, abs=0.01)

    med_prob = aggregate_temporal_predictions(probs, confs, "MEDIAN")
    assert med_prob == pytest.approx(0.60, abs=0.01)

    conf_prob = aggregate_temporal_predictions(probs, confs, "CONFIDENCE_WEIGHTED")
    assert 0.1 <= conf_prob <= 0.9


def test_multi_face_aggregation():
    face_tracks = [
        {"track_id": "face_track_1", "frame_entries": [{"fake_probability": 0.1}, {"fake_probability": 0.2}]},
        {"track_id": "face_track_2", "frame_entries": [{"fake_probability": 0.85}, {"fake_probability": 0.90}]},
    ]

    agg = aggregate_multi_face_predictions(face_tracks, "CONFIDENCE_WEIGHTED")
    assert agg.faces_analyzed_count == 2
    assert agg.highest_risk_face_id == "face_track_2"
    assert agg.overall_fake_probability >= 0.85


# ============================================================
# 4. Confidence Calibration & False Positive Protection
# ============================================================

def test_confidence_calibration_clean():
    verdict = calibrate_deepfake_confidence(
        fake_probability=0.88,
        model_confidence=0.95,
        quality_metrics={"overall_quality_score": 85},
        min_face_dimension=224,
        frames_analyzed=8,
    )
    assert verdict.is_low_confidence is False
    assert verdict.severity == "CRITICAL"
    assert verdict.risk_score == 88


def test_false_positive_protection_trigger():
    """Poor quality media or small face crops trigger LOW_CONFIDENCE state."""
    verdict = calibrate_deepfake_confidence(
        fake_probability=0.92,
        model_confidence=0.85,
        quality_metrics={"overall_quality_score": 25},  # Very low quality
        min_face_dimension=28,  # Small face crop
        frames_analyzed=1,
    )
    assert verdict.is_low_confidence is True
    assert verdict.severity == "LOW_CONFIDENCE"
    assert verdict.risk_score <= 40  # Risk score dampened for low confidence


# ============================================================
# 5. Explainability & Evidence Generation Tests
# ============================================================

def test_explainability_generation():
    verdict = calibrate_deepfake_confidence(0.85, 0.92, {"overall_quality_score": 80})
    tracks = [
        {"track_id": "face_track_1", "frame_entries": [{"fake_probability": 0.85}]},
    ]
    agg = aggregate_multi_face_predictions(tracks)

    exp = generate_deepfake_explainability(verdict, agg, "EfficientNet-B0-Deepfake", "cpu")
    assert exp["heatmap_available"] is True
    assert "facial_boundary_artifacts" in exp["feature_importance"]
    assert exp["device_used"] == "cpu"


def test_evidence_card_generation():
    verdict = calibrate_deepfake_confidence(0.85, 0.92, {"overall_quality_score": 80})
    tracks = [
        {"track_id": "face_track_1", "frame_entries": [{"fake_probability": 0.85}]},
    ]
    agg = aggregate_multi_face_predictions(tracks)

    evidence, recs = generate_deepfake_evidence_cards(verdict, agg, "EfficientNet-B0-Deepfake")
    assert len(evidence) >= 1
    assert any(e["severity"] == "CRITICAL" for e in evidence)
    assert len(recs) >= 1


# ============================================================
# 6. Master Orchestrator Integration Test
# ============================================================

@pytest.mark.asyncio
async def test_deepfake_orchestrator_neural_pipeline():
    orchestrator = DeepfakePipelineOrchestrator()
    img_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 500

    res = await orchestrator.analyze_media(img_bytes, "test_deepfake.png", "image/png")

    assert res.module == "video-deepfake"
    assert res.status == "completed"
    assert res.pipeline_status == "INFERENCE_COMPLETED"
    assert 0.0 <= res.fake_probability <= 1.0
    assert 0.0 <= res.confidence_score <= 1.0
    assert res.model_name == "EfficientNet-B0-Deepfake"
    assert "heatmap_available" in res.explainability
    assert len(res.evidence) >= 1
