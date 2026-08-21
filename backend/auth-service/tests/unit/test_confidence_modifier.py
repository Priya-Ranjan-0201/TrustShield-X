"""Unit tests for Confidence Modifiers (Phase 3.9 Part 1B)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_confidence_modifiers():
    policy = RiskPolicy()
    assert policy.CONFIDENCE_MODIFIERS["VERY_HIGH"] == 1.0
    assert policy.CONFIDENCE_MODIFIERS["LOW"] == 0.4
