"""Unit tests for Phase 3.6 Part 2A-2A-2 — AI Conversation Intelligence, Explainability & Scam Detection Engine.

Tests cover:
- ConversationIntelligenceEngine (Speaker participation, switching count, balance ratio, conversation quality)
- VoiceBehaviorAnalyzer (Speaking speed, pitch stability, speech continuity, pause distribution)
- AudioScamDetector (Rule-based detection for OTP, KYC, Bank, UPI PIN, Remote Access, Digital Arrest scams)
- AudioExplainabilityEngine (Structured explanations across categories)
- AudioEvidenceGenerator (Standardized platform evidence cards creation)
- AudioRecommendationEngine (Deterministic security recommendations)
- Master AudioProcessingOrchestrator pipeline integration
"""

import pytest
from app.services.conversation_intelligence import ConversationIntelligenceEngine
from app.services.voice_behavior_analyzer import VoiceBehaviorAnalyzer
from app.services.audio_scam_detector import AudioScamDetector
from app.services.audio_explainability import AudioExplainabilityEngine
from app.services.audio_evidence_generator import AudioEvidenceGenerator
from app.services.audio_recommendation_engine import AudioRecommendationEngine
from app.services.audio_detector import AudioProcessingOrchestrator


# ============================================================
# 1. Conversation Intelligence Engine Tests
# ============================================================

def test_conversation_intelligence_engine():
    engine = ConversationIntelligenceEngine()
    vad_segs = [
        {"is_speech": True, "duration_sec": 3.0, "speaker_id": "speaker_1"},
        {"is_speech": False, "duration_sec": 0.5, "speaker_id": "silence"},
        {"is_speech": True, "duration_sec": 2.5, "speaker_id": "speaker_2"},
    ]
    spk_tracks = [
        {"speaker_id": "speaker_1", "total_speaking_duration": 3.0, "segment_count": 1},
        {"speaker_id": "speaker_2", "total_speaking_duration": 2.5, "segment_count": 1},
    ]

    out = engine.analyze_conversation(10.0, vad_segs, spk_tracks, {"overall_quality_score": 85})

    assert out.total_speakers == 2
    assert out.speaker_switching_count == 1
    assert "speaker_1" in out.speaker_participation
    assert "speaker_2" in out.speaker_participation


# ============================================================
# 2. Voice Behavior Analyzer Tests
# ============================================================

def test_voice_behavior_analyzer():
    analyzer = VoiceBehaviorAnalyzer()
    vad_segs = [{"is_speech": True, "duration_sec": 4.0}]

    out = analyzer.analyze_behavior(vad_segs, {"overall_quality_score": 80}, 10.0)

    assert out.estimated_speaking_speed_wps > 0.0
    assert out.pitch_stability_index > 0.0
    assert out.behavior_summary["assessment_type"] == "FACTUAL_SIGNAL_DYNAMICS"


# ============================================================
# 3. Audio Scam Detector Tests
# ============================================================

def test_audio_scam_detector_rules():
    detector = AudioScamDetector()

    # Test OTP Scam match
    otp_matches = detector.detect_scam_indicators("Please share your OTP for verification")
    assert len(otp_matches) >= 1
    assert otp_matches[0].category == "OTP_FRAUD"

    # Test AnyDesk Remote Access match
    remote_matches = detector.detect_scam_indicators("Download AnyDesk or QuickSupport app")
    assert len(remote_matches) >= 1
    assert remote_matches[0].category == "REMOTE_ACCESS_SCAM"

    # Test Digital Arrest match
    police_matches = detector.detect_scam_indicators("You are under digital arrest by police")
    assert len(police_matches) >= 1
    assert police_matches[0].category == "POLICE_IMPERSONATION"


# ============================================================
# 4. Audio Explainability Engine Tests
# ============================================================

def test_audio_explainability_engine():
    engine = AudioExplainabilityEngine()
    exps = engine.generate_explanations(
        verdict="VOICE_CLONE",
        clone_probability=0.88,
        calibrated_confidence=0.92,
        quality_metrics={"snr_db": 10.0},
        speaker_tracks=[{"speaker_id": "speaker_1"}],
        similarity_metrics={"similarity_anomaly_detected": True},
        duration_sec=1.5,
    )

    assert len(exps) >= 3
    cats = [e.category for e in exps]
    assert "VOICE_SIMILARITY" in cats
    assert "LOW_AUDIO_QUALITY" in cats


# ============================================================
# 5. Evidence Generator & Recommendation Engine Tests
# ============================================================

def test_evidence_generator_and_recommendations():
    ev_gen = AudioEvidenceGenerator()
    rec_eng = AudioRecommendationEngine()

    cards = ev_gen.generate_evidence_cards(
        verdict="VOICE_CLONE",
        risk_score=85,
        calibrated_confidence=0.90,
        confidence_level="VERY_HIGH",
        explanations=[],
        scam_matches=[],
        quality_metrics={"snr_db": 28.0},
    )

    assert len(cards) >= 1
    assert cards[0]["type"] == "VOICE_CLONE"

    recs = rec_eng.generate_recommendations(cards)
    assert len(recs) >= 1
    assert "out-of-band" in recs[0].lower() or "verify" in recs[0].lower()


# ============================================================
# 6. Master Orchestrator Full Pipeline Integration Test
# ============================================================

@pytest.mark.asyncio
async def test_audio_orchestrator_conversation_intelligence():
    orchestrator = AudioProcessingOrchestrator()
    sample_wav = b"RIFF" + b"\x00" * 1000

    res = await orchestrator.analyze_audio(sample_wav, "sample.wav", "audio/wav")

    assert res.module == "audio-voice-ai"
    assert res.status == "completed"
    assert res.pipeline_status == "AI_CONVERSATION_INTELLIGENCE_COMPLETED"
    assert isinstance(res.risk_score, int)
    assert len(res.evidence) >= 1
    assert len(res.recommendations) >= 1
