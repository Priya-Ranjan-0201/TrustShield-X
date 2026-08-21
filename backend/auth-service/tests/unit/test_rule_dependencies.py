"""Unit tests for Rule Dependency Resolution (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleDTO


def test_rule_prerequisites():
    rule = BehaviorRuleDTO(
        rule_id="RULE-DEP-001",
        rule_version="1.0.0",
        namespace="DATAFLOW",
        name="Dependent Rule",
        description="Description",
        prerequisites=["MANIFEST_INTELLIGENCE", "API_INTELLIGENCE"],
    )

    assert "API_INTELLIGENCE" in rule.prerequisites
