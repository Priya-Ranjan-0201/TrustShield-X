"""Unit tests for Notification Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_notification_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="notif_1",
        finding_type="NOTIFICATION_LISTEN",
        category="DATA_COLLECTION",
        evidence_strength="STRONG",
        summary="NotificationListenerService detected",
    )

    assert f.finding_type == "NOTIFICATION_LISTEN"
