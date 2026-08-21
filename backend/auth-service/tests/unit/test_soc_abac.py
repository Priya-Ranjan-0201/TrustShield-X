import pytest
from app.services.soc.response_plan_generator import ResponsePlanGenerator


def test_soc_abac_attribute_evaluation():
    generator = ResponsePlanGenerator()

    # Normal workload
    plan_normal = generator.generate_plan("inc_abac_1", "srv_checkout")
    assert plan_normal.is_safe is True

    # Root IAM workload
    plan_root = generator.generate_plan("inc_abac_2", "srv_iam_root")
    assert plan_root.is_safe is False
