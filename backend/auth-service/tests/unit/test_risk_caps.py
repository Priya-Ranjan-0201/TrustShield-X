"""Unit tests for Risk Caps & Category Ceilings (Phase 3.9 Part 1B)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_risk_caps():
    policy = RiskPolicy()
    assert policy.MAX_SCORE == 100.0
    assert policy.MAX_CATEGORY_SCORE == 40.0
