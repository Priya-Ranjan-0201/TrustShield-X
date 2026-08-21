import pytest
from app.services.security_engineering.controlled_rollout_engine import ControlledRolloutEngine

def test_canary_escape():
    engine = ControlledRolloutEngine()
    dep = engine.deploy_change("imp_canary", strategy="CANARY")
    assert dep.status == "CANARY_ACTIVE"
    assert dep.new_state["scope"] == "canary_10pct"
