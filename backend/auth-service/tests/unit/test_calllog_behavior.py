"""Unit tests for Call Log Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_calllog_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="call_1",
        finding_type="CALLLOG_ACCESS",
        category="DATA_COLLECTION",
        evidence_strength="STRONG",
        summary="Call log reader detected",
    )

    assert f.finding_type == "CALLLOG_ACCESS"
