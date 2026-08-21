"""Unit tests for AND Logic Condition Tree Evaluation (Phase 3.9 Part 1A.24)."""

import pytest
from app.services.behavior_rule_engine import BehaviorRuleEngine
from app.schemas.behavior_rule_models import BehaviorRuleDTO, BehaviorRuleConditionDTO


def test_and_logic_evaluation():
    engine = BehaviorRuleEngine()
    rule = BehaviorRuleDTO(
        rule_id="RULE-AND-001",
        rule_version="1.0.0",
        namespace="DATAFLOW",
        name="AND Rule",
        description="Description",
        prerequisites=["API_INTELLIGENCE"],
        conditions=[
            BehaviorRuleConditionDTO(condition_id="c1", condition_type="API_CALL", expected="SmsManager", operator="AND"),
            BehaviorRuleConditionDTO(condition_id="c2", condition_type="PERMISSION_USED", expected="READ_SMS", operator="AND"),
        ],
    )

    context = {"API_INTELLIGENCE": {}}
    eval_dto, trace_dto, ev_list = engine.evaluate_rule(rule, context)

    assert eval_dto.state == "MATCHED"
    assert trace_dto.final_state == "MATCHED"
