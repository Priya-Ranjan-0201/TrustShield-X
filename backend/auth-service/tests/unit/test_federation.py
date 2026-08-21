import pytest
from app.services.collective_defense.federation_partner_registry import FederationPartnerRegistry


def test_federation_partner_lifecycle():
    registry = FederationPartnerRegistry()
    partner = registry.register_partner("ISAC Node East", trust_level=0.90, auth_key="secret_pass_key")

    assert partner.status == "ACTIVE"
    assert partner.trust_level == 0.90
    assert len(registry.list_partners()) == 1


def test_federation_rate_limiting():
    registry = FederationPartnerRegistry()
    partner = registry.register_partner("High Frequency Partner", rate_limit=3)

    assert registry.check_rate_limit(partner.partner_id) is True
    assert registry.check_rate_limit(partner.partner_id) is True
    assert registry.check_rate_limit(partner.partner_id) is True
    # Exceeds rate limit
    assert registry.check_rate_limit(partner.partner_id) is False
