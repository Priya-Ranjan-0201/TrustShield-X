import pytest
from app.services.fusion.security_health_engine import SecurityHealthEngine


def test_self_reconciliation_cycle():
    engine = SecurityHealthEngine()
    res = engine.reconcile_state_inconsistencies(
        declared_assets=[{"asset_id": "ast_1"}],
        monitoring_jobs=[{"asset_id": "ast_1", "status": "COMPLETED"}],
        tenant_id="tenant_rec",
    )
    assert res["status"] == "RECONCILED"
    assert res["inconsistencies_detected"] == 0
