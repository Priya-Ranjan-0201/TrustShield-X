"""Unit tests for Clipboard Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_clipboard_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="clip_1",
        finding_type="CLIPBOARD_READ",
        category="CLIPBOARD_DATA_FLOW",
        evidence_strength="DIRECT",
        summary="Clipboard getPrimaryClip API usage detected",
    )

    assert f.finding_type == "CLIPBOARD_READ"
