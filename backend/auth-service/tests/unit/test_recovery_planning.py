import pytest
from app.services.resilience.recovery_plan_engine import RecoveryPlanEngine

def test_recovery_planning():
    engine = RecoveryPlanEngine()
    plan = engine.generate_plan("svc_checkout_api", ["ast_net_vpc", "ast_pg_primary", "ast_api_gateway"])
    assert len(plan.steps) == 3
    assert plan.approval_tier == "TIER_2_FOUR_EYES"
    assert plan.is_approved is False
