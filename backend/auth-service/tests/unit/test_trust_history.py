import pytest
from app.services.knowledge.digital_trust_score_engine import DigitalTrustScoreEngine


def test_trust_history_transition_tracking():
    engine = DigitalTrustScoreEngine()
    profile = engine.get_or_create_profile("domain:phish-example.net", initial_risk_score=20.0, tenant_id="tenant_th")
    assert profile.trust_score >= 80.0
    assert len(profile.trust_history) == 1

    # Update trust profile after phishing discovery
    updated = engine.update_trust_profile(
        entity_id="domain:phish-example.net",
        new_trust_score=35.0,
        reason="Verified phishing campaign linkage and fraudulent credential harvest form",
        evidence_ids=["ev_phish_01", "ev_phish_02"],
        tenant_id="tenant_th",
    )
    assert updated.trust_score == 35.0
    assert len(updated.trust_history) == 2
    assert updated.trust_history[1]["previous_score"] == profile.trust_score
    assert updated.trust_history[1]["new_score"] == 35.0
