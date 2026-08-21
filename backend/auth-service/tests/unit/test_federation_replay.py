import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.federation_partner_registry import FederationPartnerRegistry


def test_federation_replay_protection():
    registry = FederationPartnerRegistry()
    partner = registry.register_partner("Partner Alpha")

    obj1 = ThreatIntelligenceObjectDTO(intelligence_type="IP", raw_indicator="198.51.100.1")
    obj2 = ThreatIntelligenceObjectDTO(intelligence_type="IP", raw_indicator="198.51.100.2")

    # Initial submission
    valid1, _ = registry.check_replay_and_poisoning(partner.partner_id, [obj1, obj2])
    assert len(valid1) == 2

    # Replay submission with duplicate obj1 and new obj3
    obj3 = ThreatIntelligenceObjectDTO(intelligence_type="IP", raw_indicator="198.51.100.3")
    valid2, _ = registry.check_replay_and_poisoning(partner.partner_id, [obj1, obj3])
    assert len(valid2) == 1
    assert valid2[0].raw_indicator == "198.51.100.3"
