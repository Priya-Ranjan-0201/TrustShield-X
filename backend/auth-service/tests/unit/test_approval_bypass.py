import pytest
from app.services.security_engineering.policy_governed_autonomy_engine import PolicyGovernedAutonomyEngine

def test_approval_bypass():
    engine = PolicyGovernedAutonomyEngine()
    can_deploy = engine.can_auto_deploy("default_tenant", "TUNE_DETECTION_THRESHOLD", blast_radius=0.1, requires_human_approval=True)
    assert can_deploy is False
