"""Unit tests for Storage Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_storage_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_stor1",
        rule_id="RULE-STORAGE-001",
        rule_version="1.0.0",
        namespace="STORAGE",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="Sensitive SharedPreference Storage",
    )

    assert eval_dto.namespace == "STORAGE"
