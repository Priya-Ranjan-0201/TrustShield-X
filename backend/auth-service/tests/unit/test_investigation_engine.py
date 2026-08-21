import pytest
from app.services.knowledge.investigation_intelligence_engine import InvestigationIntelligenceEngine


def test_investigation_session_and_recommendations():
    engine = InvestigationIntelligenceEngine()
    inv = engine.create_investigation(
        title="Operation Trojan Dropper Investigation",
        entity_ids=["apk:sha256_dropper", "domain:c2-phish.net"],
        evidence_ids=["ev_dex_01"],
        tenant_id="tenant_inv",
    )
    assert inv.investigation_id.startswith("inv_")
    assert inv.status == "ACTIVE"

    recs = engine.recommend_investigation_steps(inv.investigation_id, "tenant_inv")
    assert len(recs) >= 2
    assert recs[0].information_gain_score > 0.80

    brief = engine.generate_case_brief(inv.investigation_id, "tenant_inv")
    assert brief.investigation_id == inv.investigation_id
    assert len(brief.open_questions) >= 1
    assert len(brief.limitations) >= 1


def test_attack_story_zero_hallucination_gap_notification():
    engine = InvestigationIntelligenceEngine()
    # Timeline with only Initial Observation and Response (missing intermediate stages)
    timeline = [
        {"stage": "INITIAL_OBSERVATION", "description": "APK upload detected", "evidence_id": "ev_01"},
        {"stage": "RESPONSE", "description": "DNS Sinkhole enacted", "evidence_id": "ev_resp"},
    ]
    story = engine.generate_attack_story("INC-2026-0891", timeline)
    assert len(story.stages) == 7
    # Stages without events must explicitly declare gap rather than inventing events
    gap_stages = [s for s in story.stages if s.is_gap]
    assert len(gap_stages) == 5
    assert "No evidence available for this interval." in gap_stages[0].description
