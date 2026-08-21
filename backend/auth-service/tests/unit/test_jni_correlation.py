"""Unit tests for JNI Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_jni_correlation_dto():
    f = BehaviorFindingDTO(
        finding_id="jni_1",
        finding_type="NATIVE_NETWORK_BEHAVIOR",
        category="NATIVE_DATA_ACCESS",
        evidence_strength="STRONG",
        summary="Native socket execution via JNI bridge",
    )

    assert f.finding_type == "NATIVE_NETWORK_BEHAVIOR"
