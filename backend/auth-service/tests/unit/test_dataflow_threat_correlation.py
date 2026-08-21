"""Unit tests for Dataflow + Threat Intelligence Correlation (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatDataflowCorrelationDTO


def test_dataflow_threat_correlation_dto():
    dtc = ThreatDataflowCorrelationDTO(
        correlation_id="dtc_1",
        dataflow_path_id="path_sms_net",
        endpoint_url="https://phish.example.com",
        threat_claim="PHISHING_REPORTED",
    )

    assert dtc.dataflow_path_id == "path_sms_net"
    assert dtc.threat_claim == "PHISHING_REPORTED"
