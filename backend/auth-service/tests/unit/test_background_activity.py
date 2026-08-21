"""Unit tests for Background Activity Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_background_activity_dto():
    f = BehaviorFindingDTO(
        finding_id="bg_1",
        finding_type="BACKGROUND_NETWORK_ACTIVITY",
        category="BACKGROUND_COMMUNICATION",
        evidence_strength="STRONG",
        summary="WorkManager network task detected",
    )

    assert f.finding_type == "BACKGROUND_NETWORK_ACTIVITY"
