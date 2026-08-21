"""Unit tests for Camera Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_camera_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="cam_1",
        finding_type="CAMERA_CAPTURE",
        category="MEDIA_DATA_FLOW",
        evidence_strength="STRONG",
        summary="Camera access detected",
    )

    assert f.finding_type == "CAMERA_CAPTURE"
