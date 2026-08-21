"""Unit tests for Rule Suppression Auditing (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleSuppressionDTO


def test_rule_suppression_dto():
    sup = RuleSuppressionDTO(
        suppression_id="sup_1",
        rule_id="RULE-CRYPTO-003",
        reason="Approved corporate certificate pinning implementation",
    )

    assert sup.rule_id == "RULE-CRYPTO-003"
