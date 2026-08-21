"""Unit tests for OR Logic Condition Tree Evaluation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleConditionDTO


def test_or_logic_condition_dto():
    cond = BehaviorRuleConditionDTO(
        condition_id="c_or",
        condition_type="API_CALL",
        expected="ContentResolver",
        operator="OR",
    )

    assert cond.operator == "OR"
