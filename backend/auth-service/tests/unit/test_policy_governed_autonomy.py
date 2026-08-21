import pytest
from app.services.security_engineering.policy_governed_autonomy_engine import PolicyGovernedAutonomyEngine

def test_policy_governed_autonomy():
    engine = PolicyGovernedAutonomyEngine()
    # 1. Allowed low-risk action
    can_deploy = engine.can_auto_deploy("default_tenant", "TUNE_DETECTION_THRESHOLD", blast_radius=0.10, requires_human_approval=False)
    assert can_deploy is True

    # 2. Prohibited action
    cannot_deploy = engine.can_auto_deploy("default_tenant", "DISABLE_AUTH", blast_radius=0.01, requires_human_approval=False)
    assert cannot_deploy is False

    # 3. High blast radius requires human approval
    blocked_blast = engine.can_auto_deploy("default_tenant", "TUNE_DETECTION_THRESHOLD", blast_radius=0.45, requires_human_approval=False)
    assert blocked_blast is False
