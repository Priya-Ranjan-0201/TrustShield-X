"""Unit tests for Contact Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_contact_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="contact_1",
        finding_type="CONTACT_ACCESS",
        category="CONTACT_DATA_FLOW",
        evidence_strength="DIRECT",
        summary="ContactsContract API usage detected",
    )

    assert f.finding_type == "CONTACT_ACCESS"
