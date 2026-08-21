"""Unit tests for Prerequisite Evaluation & NOT_EVALUABLE State (Phase 3.9 Part 1A.24)."""

import pytest
from app.services.behavior_rule_engine import BehaviorRuleEngine
from app.schemas.behavior_rule_models import BehaviorRuleDTO


def test_prerequisite_missing_result():
    engine = BehaviorRuleEngine()
    rule = BehaviorRuleDTO(
        rule_id="RULE-PREREQ-001",
        rule_version="1.0.0",
        namespace="NETWORK",
        name="Prereq Test Rule",
        description="Description",
        prerequisites=["MISSING_MODULE"],
    )

    context = {}  # Missing prereq module
    eval_dto, trace_dto, ev_list = engine.evaluate_rule(rule, context)

    assert eval_dto.state == "NOT_EVALUABLE"
    assert trace_dto.final_state == "NOT_EVALUABLE"
