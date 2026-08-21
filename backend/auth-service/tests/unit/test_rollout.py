import pytest
from app.services.security_engineering.controlled_rollout_engine import ControlledRolloutEngine

def test_rollout_strategies():
    engine = ControlledRolloutEngine()
    staged = engine.deploy_change("imp_test", strategy="STAGED")
    assert staged.strategy == "STAGED"
