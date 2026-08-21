import pytest
from app.services.resilience.recovery_plan_engine import RecoveryPlanEngine

def test_recovery_approval():
    engine = RecoveryPlanEngine()
    plan = engine.generate_plan("svc_orders", ["ast_pg_orders"])
    assert plan.is_approved is False
    approved = engine.approve_plan(plan.plan_id, "usr_ciso")
    assert approved.is_approved is True
    assert approved.approver_id == "usr_ciso"
