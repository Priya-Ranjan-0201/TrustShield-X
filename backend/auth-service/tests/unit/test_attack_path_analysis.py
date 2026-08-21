import pytest
from app.services.zero_trust_exposure.attack_path_analysis_engine import AttackPathAnalysisEngine

def test_attack_path_and_ai_synthetic_rejection():
    engine = AttackPathAnalysisEngine()
    
    # Real deterministic path with evidence
    path1 = engine.analyze_path(
        path_id="PATH-01",
        tenant_id="tenant-alpha",
        entry_point="EXT-1",
        target_crown_jewel="DB-VAULT",
        path_type="NETWORK",
        nodes=["EXT-1", "APP-PROD", "DB-VAULT"],
        edges=[{"from": "EXT-1", "to": "APP-PROD"}, {"from": "APP-PROD", "to": "DB-VAULT"}],
        evidence=[{"reachability_proven": True}],
        is_ai_generated=False
    )
    assert path1["feasibility"] == "VERIFIED"
    assert path1["validation_status"] == "DETERMINISTIC_PROOF_CONFIRMED"
    
    # AI generated speculative path without proof -> UNVERIFIED
    path2 = engine.analyze_path(
        path_id="PATH-02",
        tenant_id="tenant-alpha",
        entry_point="EXT-1",
        target_crown_jewel="DB-VAULT",
        path_type="SPECULATIVE",
        nodes=["EXT-1", "UNKNOWN", "DB-VAULT"],
        edges=[],
        evidence=[],
        is_ai_generated=True
    )
    assert path2["feasibility"] == "SPECULATIVE"
    assert path2["validation_status"] == "AI_PATH_UNVERIFIED"
