"""Unit tests for Centralized Risk Policy (Phase 3.9 Part 1B)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_risk_policy_defaults():
    policy = RiskPolicy()
    assert policy.POLICY_VERSION == "1.0.0"
    assert policy.BAND_THRESHOLDS["TRUSTED"] == (0.0, 20.0)
    assert policy.CONFIDENCE_MODIFIERS["HIGH"] == 0.9
