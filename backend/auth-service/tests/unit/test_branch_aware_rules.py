"""Unit tests for Branch-Aware Control-Flow Rule Evaluation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleConditionResultDTO


def test_branch_aware_condition_result_dto():
    cr = RuleConditionResultDTO(
        condition_id="c_branch",
        condition_type="DATAFLOW_PATH",
        expected="CONDITIONAL_TRANSMISSION",
        actual="POSSIBLE_PATH_B",
        matched=True,
        reason="Evaluated under conditional execution path B",
    )

    assert cr.reason == "Evaluated under conditional execution path B"
