"""Unit tests for Behavior Rule Schema (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleDTO


def test_rule_dto():
    rule = BehaviorRuleDTO(
        rule_id="RULE-DATAFLOW-001",
        rule_version="1.0.0",
        namespace="DATAFLOW",
        name="Sensitive SMS Data Reaches Network Sink",
        description="Detects SMS permission and SMS API data flowing to a network endpoint.",
        status="ACTIVE",
    )

    assert rule.rule_id == "RULE-DATAFLOW-001"
    assert rule.namespace == "DATAFLOW"
