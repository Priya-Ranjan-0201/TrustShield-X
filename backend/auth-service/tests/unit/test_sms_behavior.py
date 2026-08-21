"""Unit tests for SMS Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_sms_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="sms_1",
        finding_type="SMS_ACCESS_BEHAVIOR",
        category="SMS_DATA_FLOW",
        evidence_strength="DIRECT",
        summary="SMS API calls detected",
    )

    assert f.finding_type == "SMS_ACCESS_BEHAVIOR"
