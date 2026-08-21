"""Unit tests for NOT Logic Condition Tree Evaluation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleConditionDTO


def test_not_logic_condition_dto():
    cond = BehaviorRuleConditionDTO(
        condition_id="c_not",
        condition_type="TLS_CONFIGURATION",
        expected="ALLOW_ALL_HOSTNAME_VERIFIER",
        operator="NOT",
    )

    assert cond.operator == "NOT"
