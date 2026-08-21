"""Unit tests for Component + Intent Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorRelationshipDTO


def test_component_intent_relationship_dto():
    rel = BehaviorRelationshipDTO(
        source_entity_id="com.bank.LoginActivity",
        target_entity_id="com.bank.MainActivity",
        relationship_type="TRIGGERS_COMPONENT",
    )

    assert rel.relationship_type == "TRIGGERS_COMPONENT"
