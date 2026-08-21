"""Unit tests for Reflection Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_reflection_correlation_dto():
    f = BehaviorFindingDTO(
        finding_id="ref_1",
        finding_type="REFLECTION_BOUNDARY",
        category="DYNAMIC_CODE_ACCESS",
        evidence_strength="MODERATE",
        confidence="MEDIUM",
        resolution_status="UNRESOLVED",
        summary="Unresolved reflection invocation target",
    )

    assert f.finding_type == "REFLECTION_BOUNDARY"
    assert f.resolution_status == "UNRESOLVED"
