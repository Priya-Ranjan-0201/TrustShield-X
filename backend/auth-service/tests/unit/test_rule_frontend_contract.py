"""Unit tests for Behavior Rules Frontend Contract DTOs (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleCardDTO


def test_rule_card_dto():
    card = RuleCardDTO(
        card_id="card_1",
        title="Sensitive SMS Data Reaches Network Sink",
        rule_id="RULE-DATAFLOW-001",
        state="MATCHED",
        confidence="HIGH",
    )

    assert card.title == "Sensitive SMS Data Reaches Network Sink"
    assert card.state == "MATCHED"
