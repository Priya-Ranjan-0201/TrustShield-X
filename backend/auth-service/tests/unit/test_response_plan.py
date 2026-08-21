import pytest
from app.services.soc.response_plan_generator import ResponsePlanGenerator


def test_response_plan_generation_structure():
    generator = ResponsePlanGenerator()
    plan = generator.generate_plan("inc_plan_01", "srv_compromised_node", "MALWARE_PROPAGATION")

    assert plan.target == "srv_compromised_node"
    assert len(plan.steps) == 4
    assert len(plan.rollback_steps) == 2
    assert plan.required_approval_tier == "TIER_2_FOUR_EYES"
    assert plan.is_safe is True
