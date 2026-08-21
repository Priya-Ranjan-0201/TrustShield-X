import pytest
from app.services.security_engineering.controlled_rollout_engine import ControlledRolloutEngine

def test_canary_deployment():
    engine = ControlledRolloutEngine()
    dep = engine.deploy_change("imp_test", strategy="CANARY")
    assert dep.status == "CANARY_ACTIVE"
    assert dep.strategy == "CANARY"
    assert dep.rollback_handle is not None
