import pytest
from app.services.security_engineering.policy_governed_autonomy_engine import PolicyGovernedAutonomyEngine

def test_improvement_rbac():
    engine = PolicyGovernedAutonomyEngine()
    cfg = engine.get_config("default_tenant")
    assert "TUNE_DETECTION_THRESHOLD" in cfg.allowed_actions
    assert "DISABLE_AUTH" in cfg.prohibited_actions
