import pytest
from app.services.soc.response_plan_generator import ResponsePlanGenerator


def test_response_plan_safety_protected_targets():
    generator = ResponsePlanGenerator()

    # Target is critical audit ledger infrastructure -> marked unsafe & risk 99
    plan = generator.generate_plan("inc_safe_01", "srv_audit_ledger")
    assert plan.is_safe is False
    assert plan.risk_score == 99.0
