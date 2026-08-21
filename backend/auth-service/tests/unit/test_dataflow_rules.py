"""Unit tests for Dataflow Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_dataflow_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_df1",
        rule_id="RULE-DATAFLOW-001",
        rule_version="1.0.0",
        namespace="DATAFLOW",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="SMS Dataflow Path",
    )

    assert eval_dto.rule_id == "RULE-DATAFLOW-001"
    assert eval_dto.state == "MATCHED"
