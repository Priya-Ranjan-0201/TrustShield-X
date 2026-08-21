"""Unit tests for Contradictory Rule Conflict Resolution (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleConflictDTO


def test_rule_conflict_dto():
    conflict = RuleConflictDTO(
        conflict_id="conf_1",
        rule_a_id="RULE-CRYPTO-002",
        rule_b_id="RULE-NETWORK-001",
        reason="Branch A sends encrypted while Branch B sends plaintext",
    )

    assert conflict.rule_a_id == "RULE-CRYPTO-002"
