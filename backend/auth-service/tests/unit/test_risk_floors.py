"""Unit tests for Risk Minimum Floors (Phase 3.9 Part 1B)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_risk_floors():
    policy = RiskPolicy()
    assert policy.MIN_SCORE == 0.0
