"""Unit tests for Phase 3.6 Part 2A-2A-1 — Advanced Confidence Calibration, Risk Aggregation & Decision Intelligence Engine.

Tests cover:
- AudioConfidenceCalibrator (Multi-variable penalties, boosts, VERY_HIGH to VERY_LOW levels)
- AudioRiskEngine (0-100 risk score calculation & configurable severity thresholds)
- AudioSpeakerAggregator (Speaker & conversation aggregation)
- AudioDecisionEngine (Verdict synthesis: REAL, VOICE_CLONE, LIKELY_CLONE, LOW_CONFIDENCE, INCONCLUSIVE)
- Ensemble Voting Strategies (Majority, Weighted, Confidence Weighted, Bayesian)
- False Positive Protection (Automatic LOW_CONFIDENCE fallback)
- Master AudioProcessingOrchestrator integration
"""

import pytest
from app.services.audio_confidence_calibrator import AudioConfidenceCalibrator
from app.services.audio_risk_engine import AudioRiskEngine, AudioRiskConfig
from app.services.audio_speaker_aggregator import AudioSpeakerAggregator
from app.services.audio_decision_engine import AudioDecisionEngine
from app.services.audio_ensemble_interface import (
    ModelVoteOutput,
    MajorityVoteEnsemble,
    WeightedVoteEnsemble,
    ConfidenceWeightedEnsemble,
    BayesianEnsemble,
)
from app.services.audio_detector import AudioProcessingOrchestrator


# ============================================================
# 1. Confidence Calibration Engine Tests
# ============================================================

def test_confidence_calibrator_high_quality():
    calibrator = AudioConfidenceCalibrator()
    res = calibrator.calibrate_confidence(
        raw_clone_probability=0.88,
        quality_metrics={"snr_db": 28.0, "clipping_ratio_percent": 0.0},
        metadata={"sample_rate": 44100},
        speech_duration_sec=12.0,
        segment_count=4,
    )
    assert res.calibrated_confidence >= 0.90
    assert res.confidence_level == "VERY_HIGH"
    assert "high_snr_boost" in res.adjustment_breakdown


def test_confidence_calibrator_low_quality_penalty():
    calibrator = AudioConfidenceCalibrator()
    res = calibrator.calibrate_confidence(
        raw_clone_probability=0.88,
        quality_metrics={"snr_db": 8.0, "clipping_ratio_percent": 5.0},
        metadata={"sample_rate": 8000},
        speech_duration_sec=1.0,
        segment_count=1,
    )
    assert res.calibrated_confidence < 0.60
    assert res.confidence_level in ("LOW", "VERY_LOW")
    assert "short_speech_penalty" in res.adjustment_breakdown


# ============================================================
# 2. Risk Aggregation Engine Tests
# ============================================================

def test_risk_engine_thresholds():
    engine = AudioRiskEngine()
    
    trusted_out = engine.compute_risk_score(0.05, 0.95, 0.05, 0.05)
    assert trusted_out.risk_score <= 20
    assert trusted_out.severity == "TRUSTED"

    critical_out = engine.compute_risk_score(0.92, 0.95, 0.95, 0.90)
    assert critical_out.risk_score >= 81
    assert critical_out.severity == "CRITICAL"


# ============================================================
# 3. Speaker Aggregator Tests
# ============================================================

def test_speaker_aggregator():
    aggregator = AudioSpeakerAggregator()
    speakers = [
        {"speaker_id": "speaker_1", "clone_probability": 0.85, "speaking_duration": 5.0},
        {"speaker_id": "speaker_2", "clone_probability": 0.15, "speaking_duration": 4.0},
    ]
    res = aggregator.aggregate_speakers(speakers, 0.90)
    assert res.highest_risk_speaker == "speaker_1"
    assert res.highest_risk_score == 0.85
    assert res.speaker_count == 2


# ============================================================
# 4. Conversation Decision Engine Tests
# ============================================================

def test_decision_engine_verdicts():
    engine = AudioDecisionEngine()

    # Voice Clone Verdict
    clone_dec = engine.make_decision(85, 0.92, "VERY_HIGH", 0.88, {"snr_db": 28.0}, 10.0)
    assert clone_dec.verdict == "VOICE_CLONE"

    # Real Voice Verdict
    real_dec = engine.make_decision(15, 0.95, "VERY_HIGH", 0.15, {"snr_db": 28.0}, 10.0)
    assert real_dec.verdict == "REAL"

    # Low Confidence Verdict (Short duration)
    low_dec = engine.make_decision(85, 0.40, "LOW", 0.88, {"snr_db": 8.0}, 1.0)
    assert low_dec.verdict == "LOW_CONFIDENCE"


# ============================================================
# 5. Ensemble Architecture Strategy Tests
# ============================================================

def test_ensemble_voting_strategies():
    votes = [
        ModelVoteOutput("ECAPA-TDNN", "CLONE", 0.88, 0.90, weight=1.0),
        ModelVoteOutput("SpeechBrain", "CLONE", 0.82, 0.85, weight=1.0),
        ModelVoteOutput("WavLM", "REAL", 0.20, 0.80, weight=0.8),
    ]

    maj = MajorityVoteEnsemble()
    maj_out = maj.aggregate_votes(votes)
    assert maj_out.winning_label == "CLONE"

    weighted = WeightedVoteEnsemble()
    w_out = weighted.aggregate_votes(votes)
    assert w_out.winning_label == "CLONE"

    bayes = BayesianEnsemble()
    b_out = bayes.aggregate_votes(votes)
    assert b_out.winning_label == "CLONE"


# ============================================================
# 6. Master Orchestrator Decision Intelligence Integration
# ============================================================

@pytest.mark.asyncio
async def test_audio_orchestrator_decision_intelligence():
    orchestrator = AudioProcessingOrchestrator()
    sample_wav = b"RIFF" + b"\x00" * 1000

    res = await orchestrator.analyze_audio(sample_wav, "sample.wav", "audio/wav")

    assert res.module == "audio-voice-ai"
    assert res.status == "completed"
    assert res.pipeline_status == "AI_CONVERSATION_INTELLIGENCE_COMPLETED"
    assert isinstance(res.risk_score, int)
    assert isinstance(res.confidence_score, float)
    assert len(res.evidence) >= 1
