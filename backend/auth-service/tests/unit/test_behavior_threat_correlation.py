"""Unit tests for Behavior + Threat Intelligence Correlation (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatBehaviorCorrelationDTO


def test_behavior_threat_correlation_dto():
    btc = ThreatBehaviorCorrelationDTO(
        correlation_id="btc_1",
        behavior_type="SMS_DATA_NETWORK_FLOW",
        indicator_value="ind_phish_url",
        threat_claim="PHISHING_REPORTED",
    )

    assert btc.behavior_type == "SMS_DATA_NETWORK_FLOW"
    assert btc.threat_claim == "PHISHING_REPORTED"
