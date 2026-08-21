"""Unit tests for Accessibility Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_accessibility_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="access_1",
        finding_type="ACCESSIBILITY_DATA_ACCESS",
        category="DATA_COLLECTION",
        evidence_strength="DIRECT",
        summary="AccessibilityService window content access detected",
    )

    assert f.finding_type == "ACCESSIBILITY_DATA_ACCESS"
