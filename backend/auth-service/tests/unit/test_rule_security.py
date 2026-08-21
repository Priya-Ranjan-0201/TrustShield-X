"""Unit tests for Declarative-Only Code Execution & Security Controls (Phase 3.9 Part 1A.24)."""

import pytest
from app.services.rule_validator import RuleValidator
from app.schemas.behavior_rule_models import BehaviorRuleDTO, BehaviorRuleConditionDTO


def test_reject_unbounded_rule_conditions():
    validator = RuleValidator()
    too_many_conds = [BehaviorRuleConditionDTO(condition_id=f"c_{i}", condition_type="API_CALL", expected="Test") for i in range(100)]
    rule = BehaviorRuleDTO(
        rule_id="RULE-UNBOUNDED-001",
        rule_version="1.0.0",
        namespace="NETWORK",
        name="Pathological Rule",
        description="Unbounded rule",
        conditions=too_many_conds,
    )

    assert validator.validate_rule(rule) is False
