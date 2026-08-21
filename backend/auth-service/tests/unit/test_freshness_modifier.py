"""Unit tests for Threat Freshness Modifiers (Phase 3.9 Part 1B)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_freshness_modifiers():
    policy = RiskPolicy()
    assert policy.FRESHNESS_MODIFIERS["CURRENT"] == 1.0
    assert policy.FRESHNESS_MODIFIERS["EXPIRED"] == 0.1
