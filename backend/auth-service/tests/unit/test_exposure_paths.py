import pytest
from app.services.zero_trust_exposure.attack_path_analysis_engine import AttackPathAnalysisEngine

def test_exposure_path_modeling():
    engine = AttackPathAnalysisEngine()
    nodes = [
        {"id": "INTERNET", "type": "NETWORK"},
        {"id": "PUBLIC_API", "type": "SERVICE"},
        {"id": "CVE-2024-3094", "type": "VULNERABILITY"},
        {"id": "SVC_ACCOUNT", "type": "CREDENTIAL"},
        {"id": "RESTRICTED_DB", "type": "RESOURCE"}
    ]
    edges = [
        {"source": "INTERNET", "target": "PUBLIC_API", "type": "REACHES"},
        {"source": "PUBLIC_API", "target": "CVE-2024-3094", "type": "EXPOSES"},
        {"source": "CVE-2024-3094", "target": "SVC_ACCOUNT", "type": "DEPENDS_ON"},
        {"source": "SVC_ACCOUNT", "target": "RESTRICTED_DB", "type": "ACCESSES"}
    ]
    path = engine.analyze_path(
        path_id="EXP-PATH-100",
        tenant_id="t1",
        entry_point="INTERNET",
        target_crown_jewel="RESTRICTED_DB",
        nodes=nodes,
        edges=edges,
        evidence=[{"reachability_confirmed": True}]
    )
    assert len(path["nodes"]) == 5
    assert len(path["edges"]) == 4
    assert path["status"] == "VERIFIED"
