import pytest
from app.services.federation.intelligence_corroboration_engine import IntelligenceCorroborationEngine


def test_intelligence_verification_progression():
    engine = IntelligenceCorroborationEngine()

    # 1. Single observation -> OBSERVED
    r1 = engine.evaluate_corroboration("phish-target.com", [{"source_id": "src_1", "source_reliability": 0.85}])
    assert r1["verification_status"] == "OBSERVED"

    # 2. Multi-source independent corroboration -> VERIFIED
    r2 = engine.evaluate_corroboration("phish-target.com", [
        {"source_id": "src_1", "source_reliability": 0.95},
        {"source_id": "src_2", "source_reliability": 0.92},
        {"source_id": "src_3", "source_reliability": 0.90},
    ])
    assert r2["verification_status"] == "VERIFIED"
    assert r2["confidence_score"] >= 0.90
