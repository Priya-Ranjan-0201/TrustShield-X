"""Unit tests for Rule Condition Evaluation Engine (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleConditionResultDTO


def test_condition_result_dto():
    cr = RuleConditionResultDTO(
        condition_id="c1",
        condition_type="PERMISSION_USED",
        expected="android.permission.READ_SMS",
        actual="android.permission.READ_SMS",
        matched=True,
    )

    assert cr.matched is True
