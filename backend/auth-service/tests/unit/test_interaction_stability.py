"""Unit tests for Composite Risk Interaction Stability (Phase 3.9 Part 1C)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_interaction_stability():
    policy = RiskPolicy()
    assert policy.MAX_INTERACTION_BONUS == 15.0
