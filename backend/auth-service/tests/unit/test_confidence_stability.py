"""Unit tests for Confidence Level Stability (Phase 3.9 Part 1C)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_confidence_stability():
    policy = RiskPolicy()
    assert policy.CONFIDENCE_MODIFIERS["HIGH"] == 0.9
