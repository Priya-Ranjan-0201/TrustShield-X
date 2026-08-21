import pytest
from app.services.collective_defense.federation_partner_registry import FederationPartnerRegistry


def test_federation_authentication_success_and_failure():
    registry = FederationPartnerRegistry()
    partner = registry.register_partner("Partner Secure", auth_key="correct_token_123")

    assert registry.authenticate_partner(partner.partner_id, "correct_token_123") is True
    assert registry.authenticate_partner(partner.partner_id, "wrong_token") is False
    assert registry.authenticate_partner("non_existent_id", "correct_token_123") is False
