import pytest
from app.services.security_engineering.controlled_rollout_engine import ControlledRolloutEngine
from app.services.security_engineering.security_rollback_engine import SecurityRollbackEngine

def test_rollback_failure():
    rollout = ControlledRolloutEngine()
    dep = rollout.deploy_change("imp_fail", strategy="CANARY")
    rbk = SecurityRollbackEngine()
    rec = rbk.execute_rollback(dep)
    assert rec.rollback_verified is True
