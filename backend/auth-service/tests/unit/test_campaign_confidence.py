import pytest
from app.schemas.threat_intelligence_fabric_models import CampaignClusterDTO


def test_campaign_confidence_metrics():
    camp = CampaignClusterDTO(
        name="Operation Test",
        confidence=0.91,
        attribution_confidence="ASSESSED",
    )
    assert 0.0 <= camp.confidence <= 1.0
    assert camp.attribution_confidence == "ASSESSED"
