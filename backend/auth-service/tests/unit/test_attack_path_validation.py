import pytest
from app.services.zero_trust_exposure.attack_path_analysis_engine import AttackPathAnalysisEngine

def test_attack_path_reachability_unverified_fallback():
    engine = AttackPathAnalysisEngine()
    path = engine.analyze_path(
        path_id="PATH-HYPO-1",
        tenant_id="t1",
        entry_point="internet",
        target_crown_jewel="database",
        evidence=[]
    )
    assert path["status"] == "ATTACK_PATH_UNVERIFIED"
    assert path["reachability_verified"] is False
