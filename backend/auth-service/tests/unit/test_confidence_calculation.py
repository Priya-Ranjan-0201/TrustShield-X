"""Unit tests for Rule Confidence Calculation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_confidence_level_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_conf1",
        rule_id="RULE-NETWORK-001",
        rule_version="1.0.0",
        namespace="NETWORK",
        state="MATCHED",
        confidence="VERY_HIGH",
        evidence_provenance="Direct Network Packet Inspection",
    )

    assert eval_dto.confidence == "VERY_HIGH"
