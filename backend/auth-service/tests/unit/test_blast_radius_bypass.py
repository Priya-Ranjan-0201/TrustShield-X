import pytest
from app.services.security_engineering.policy_governed_autonomy_engine import PolicyGovernedAutonomyEngine

def test_blast_radius_bypass():
    engine = PolicyGovernedAutonomyEngine()
    can_deploy = engine.can_auto_deploy("default_tenant", "TUNE_DETECTION_THRESHOLD", blast_radius=0.75, requires_human_approval=False)
    assert can_deploy is False
