import pytest
from app.services.zero_trust_exposure.attack_path_analysis_engine import AttackPathAnalysisEngine

def test_attack_path_risk_verified():
    engine = AttackPathAnalysisEngine()
    path = engine.analyze_path(
        path_id="PATH-VERIFIED-1",
        tenant_id="t1",
        entry_point="ext-api",
        target_crown_jewel="vault",
        path_type="HYBRID",
        evidence=[{"reachability_confirmed": True, "probe_latency_ms": 12}]
    )
    assert path["status"] == "VERIFIED"
    assert path["risk_score"] >= 8.5
