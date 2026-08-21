"""Unit tests for IOC Deduplication (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatIndicatorDTO


def test_indicator_deduplication_dto():
    ind1 = ThreatIndicatorDTO(
        indicator_id="ind_1",
        indicator_type="DOMAIN",
        normalized_value="example.com",
        display_value="example.com",
        value_hash="hash_1",
        source_module="NET",
        source_location="com.bank.Net",
    )
    ind2 = ThreatIndicatorDTO(
        indicator_id="ind_1",
        indicator_type="DOMAIN",
        normalized_value="example.com",
        display_value="example.com",
        value_hash="hash_1",
        source_module="NET_2",
        source_location="com.bank.Net2",
    )

    assert ind1.normalized_value == ind2.normalized_value
