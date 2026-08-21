"""Unit tests for Component Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_component_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_comp1",
        rule_id="RULE-COMPONENT-001",
        rule_version="1.0.0",
        namespace="COMPONENTS",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="Exported Activity Entry Point",
    )

    assert eval_dto.namespace == "COMPONENTS"
