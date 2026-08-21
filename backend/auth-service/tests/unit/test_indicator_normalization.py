"""Unit tests for Indicator Normalization Engine (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatIndicatorDTO


def test_indicator_normalization_dto():
    ind = ThreatIndicatorDTO(
        indicator_id="ind_1",
        indicator_type="DOMAIN",
        normalized_value="example.com",
        display_value="EXAMPLE.COM.",
        value_hash="hash_1",
        source_module="NETWORK",
        source_location="com.bank.Net",
    )

    assert ind.normalized_value == "example.com"
