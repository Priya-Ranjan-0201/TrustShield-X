"""Unit tests for Policy Sensitivity Analysis (Phase 3.9 Part 1C)."""

import pytest
from app.core.risk_policy import RiskPolicy


def test_policy_sensitivity_parameters():
    policy = RiskPolicy()
    assert policy.POLICY_VERSION == "1.0.0"
