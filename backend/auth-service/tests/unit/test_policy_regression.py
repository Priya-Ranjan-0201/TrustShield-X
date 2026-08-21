"""Unit tests for Policy Version Regression Testing (Phase 3.9 Part 1C)."""

import pytest
from app.schemas.risk_aggregation_models import RiskPolicyVersionDTO


def test_policy_regression_version():
    ver = RiskPolicyVersionDTO(policy_version="1.0.0")
    assert ver.policy_version == "1.0.0"
