"""Unit tests for Risk Weight Registry (Phase 3.9 Part 1B)."""

import pytest
from app.core.risk_weight_registry import RiskWeightRegistry


def test_weight_registry_lookup():
    registry = RiskWeightRegistry()
    cfg = registry.get_weight_config("SMS_DATA_NETWORK_TRANSFER")

    assert cfg is not None
    assert cfg["category"] == "DATA_EXFILTRATION"
    assert cfg["base_weight"] == 25.0
