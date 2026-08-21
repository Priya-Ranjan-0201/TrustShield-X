"""Unit tests for Threshold Condition Evaluation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleConditionDTO


def test_threshold_condition_dto():
    cond = BehaviorRuleConditionDTO(
        condition_id="c_thresh",
        condition_type="API_CALL_COUNT",
        expected=">= 5",
        operator="AT_LEAST",
    )

    assert cond.operator == "AT_LEAST"
