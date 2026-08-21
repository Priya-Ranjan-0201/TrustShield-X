"""Unit tests for Risk Ceilings Validation (Phase 3.9 Part 1C)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_risk_caps_validation():
    policy = RiskPolicy()
    assert policy.UNRESOLVED_REFLECTION_CAP == 60.0
    assert policy.UNRESOLVED_JNI_CAP == 60.0
