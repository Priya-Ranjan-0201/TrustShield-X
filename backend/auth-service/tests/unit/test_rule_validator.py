"""Unit tests for Rule Validator (Phase 3.9 Part 1A.24)."""

import pytest
from app.services.rule_validator import RuleValidator
from app.schemas.behavior_rule_models import BehaviorRuleDTO


def test_rule_validator():
    validator = RuleValidator()
    rule = BehaviorRuleDTO(
        rule_id="RULE-TEST-001",
        rule_version="1.0.0",
        namespace="NETWORK",
        name="Test Rule",
        description="Description",
    )

    assert validator.validate_rule(rule) is True
