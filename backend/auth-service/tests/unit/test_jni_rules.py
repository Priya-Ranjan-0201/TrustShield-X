"""Unit tests for JNI Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_jni_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_j1",
        rule_id="RULE-JNI-001",
        rule_version="1.0.0",
        namespace="JNI",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="JNI Native Method Registration",
    )

    assert eval_dto.namespace == "JNI"
