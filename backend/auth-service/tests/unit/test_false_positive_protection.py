"""Unit tests for False-Positive Protection Safeguards (Phase 3.9 Part 1A.23)."""

import pytest
from app.services.threat_intelligence_service import ThreatIntelligenceService
from app.schemas.network_models import NetworkIntelligenceResultDTO, NetworkEndpointDTO


def test_no_premature_malware_verdict():
    service = ThreatIntelligenceService()
    net_dto = NetworkIntelligenceResultDTO(
        endpoints=[
            NetworkEndpointDTO(
                endpoint_id="ep_1",
                url="https://clean.example.com",
                domain="clean.example.com",
                host="clean.example.com",
                source_class="com.example.Net",
                source_method="get",
            )
        ]
    )

    res = service.analyze_threat_intelligence(network_intelligence_dto=net_dto)

    # Must NOT generate final risk scores or premature malware verdicts
    for m in res.matches:
        assert "MALWARE_VERDICT" not in m.match_type
        assert "FINAL_RISK_SCORE" not in m.match_type
