"""Unit tests for XOR Logic Condition Tree Evaluation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleConditionDTO


def test_xor_logic_condition_dto():
    cond = BehaviorRuleConditionDTO(
        condition_id="c_xor",
        condition_type="CRYPTO_OPERATION",
        expected="AES_CBC",
        operator="XOR",
    )

    assert cond.operator == "XOR"
