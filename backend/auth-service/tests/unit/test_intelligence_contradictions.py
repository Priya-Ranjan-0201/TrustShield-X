import pytest
from app.services.threat_intelligence.corroboration_contradiction_engine import CorroborationContradictionEngine


def test_contradiction_detection_preserves_both_claims():
    engine = CorroborationContradictionEngine()

    claims = [
        {"source_id": "src_vendor_a", "reputation": "MALICIOUS"},
        {"source_id": "src_vendor_b", "reputation": "BENIGN"},
    ]
    res = engine.evaluate_corroboration(claims)

    assert res["status"] == "CONFLICTING_INTELLIGENCE"
    assert len(res["conflicts"]) == 1
    assert res["preserves_all_claims"] is True
