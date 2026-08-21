import pytest
from app.services.threat_intelligence.campaign_discovery_engine import CampaignDiscoveryEngine


def test_campaign_discovery_clustering():
    engine = CampaignDiscoveryEngine()
    camp = engine.get_campaign("camp_shadowstrike")

    assert camp is not None
    assert camp.name == "Operation ShadowStrike"
    assert len(camp.infrastructure) >= 2
    assert "FINANCIAL_SERVICES" in camp.targeted_sectors
