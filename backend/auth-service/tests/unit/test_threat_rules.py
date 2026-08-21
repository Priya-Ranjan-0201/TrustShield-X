"""Unit tests for Threat Intelligence Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_threat_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_th1",
        rule_id="RULE-THREAT-001",
        rule_version="1.0.0",
        namespace="THREAT_INTELLIGENCE",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="Known Phishing Endpoint IOC",
    )

    assert eval_dto.namespace == "THREAT_INTELLIGENCE"
