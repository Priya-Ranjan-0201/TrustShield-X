import pytest
from app.services.threat_intelligence.corroboration_contradiction_engine import CorroborationContradictionEngine


def test_independent_corroboration_multi_source():
    engine = CorroborationContradictionEngine()

    claims = [
        {"source_id": "src_crowdstrike", "reputation": "MALICIOUS"},
        {"source_id": "src_misp", "reputation": "MALICIOUS"},
    ]
    res = engine.evaluate_corroboration(claims)

    assert res["corroborating_source_count"] == 2
    assert res["status"] == "CORROBORATED"
