import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.federation_partner_registry import FederationPartnerRegistry


def test_intelligence_poisoning_surge_detected():
    registry = FederationPartnerRegistry()
    partner = registry.register_partner("Anomalous Node", trust_level=0.80)

    # Generate huge flood of 501 items
    flood = [
        ThreatIntelligenceObjectDTO(intelligence_type="DOMAIN", raw_indicator=f"fake-spam-domain-{i}.com")
        for i in range(505)
    ]

    valid, _ = registry.check_replay_and_poisoning(partner.partner_id, flood)
    alerts = registry.list_poisoning_alerts()

    assert len(alerts) >= 1
    assert "INTELLIGENCE_POISONING_WARNING" in alerts[0]["warning"]
    assert partner.status == "PROBATION"
    assert partner.trust_level < 0.80
