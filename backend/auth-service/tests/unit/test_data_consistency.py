import pytest
from app.services.fusion.security_health_engine import SecurityHealthEngine


def test_data_consistency_and_state_contradiction_detection():
    engine = SecurityHealthEngine()

    declared = [{"asset_id": "ast_active_01"}]
    # Monitoring job references deleted asset ast_deleted_99
    monitoring = [{"asset_id": "ast_active_01", "status": "RUNNING"}, {"asset_id": "ast_deleted_99", "status": "RUNNING"}]

    res = engine.reconcile_state_inconsistencies(declared, monitoring, "tenant_cons")
    assert res["inconsistencies_detected"] == 1
    assert res["repaired_actions"][0]["issue"] == "ORPHAN_MONITORING_JOB"
    assert res["repaired_actions"][0]["asset_id"] == "ast_deleted_99"
