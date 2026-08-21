"""Unit tests for N-of-M Threshold Logic Evaluation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleConditionDTO


def test_n_of_m_condition_dto():
    cond = BehaviorRuleConditionDTO(
        condition_id="c_nom",
        condition_type="BEHAVIOR_FINDING",
        expected="2_OF_3_SUSPICIOUS",
        operator="N_OF_M",
    )

    assert cond.operator == "N_OF_M"
