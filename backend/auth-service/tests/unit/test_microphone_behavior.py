"""Unit tests for Microphone & Audio Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_microphone_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="mic_1",
        finding_type="AUDIO_CAPTURE",
        category="MEDIA_DATA_FLOW",
        evidence_strength="STRONG",
        summary="Audio recording detected",
    )

    assert f.finding_type == "AUDIO_CAPTURE"
