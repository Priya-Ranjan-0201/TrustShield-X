"""Unit tests for Composite Multi-Module Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_composite_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_comp_rule1",
        rule_id="RULE-COMPOSITE-001",
        rule_version="1.0.0",
        namespace="COMPOSITE",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="SMS Permission + Dataflow + Threat Indicator",
    )

    assert eval_dto.namespace == "COMPOSITE"
