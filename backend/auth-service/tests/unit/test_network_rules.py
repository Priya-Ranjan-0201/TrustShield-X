"""Unit tests for Network Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_network_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_net1",
        rule_id="RULE-NETWORK-001",
        rule_version="1.0.0",
        namespace="NETWORK",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="Static Network Endpoint",
    )

    assert eval_dto.namespace == "NETWORK"
