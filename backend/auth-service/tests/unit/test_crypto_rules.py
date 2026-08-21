"""Unit tests for Cryptography Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_crypto_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_c1",
        rule_id="RULE-CRYPTO-001",
        rule_version="1.0.0",
        namespace="CRYPTOGRAPHY",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="Cipher Operation",
    )

    assert eval_dto.namespace == "CRYPTOGRAPHY"
