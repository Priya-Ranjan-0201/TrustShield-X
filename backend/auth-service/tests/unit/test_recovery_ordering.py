import pytest
from app.services.resilience.recovery_plan_engine import RecoveryPlanEngine

def test_recovery_ordering():
    engine = RecoveryPlanEngine()
    plan = engine.get_plan("recplan_checkout_recovery")
    assert plan is not None
    assert plan.recovery_order == ["ast_net_vpc", "ast_pg_primary", "ast_redis_cache", "ast_api_gateway"]
