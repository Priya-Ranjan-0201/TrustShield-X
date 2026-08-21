"""Unit tests for Third-Party SDK Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_third_party_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_tp1",
        rule_id="RULE-THIRDPARTY-001",
        rule_version="1.0.0",
        namespace="THIRDPARTY",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="Analytics SDK Transfer",
    )

    assert eval_dto.namespace == "THIRDPARTY"
