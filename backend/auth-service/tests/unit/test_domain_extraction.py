"""Unit tests for Domain Intelligence Extraction (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkDomainDTO


def test_domain_dto():
    dom = NetworkDomainDTO(
        domain="api.bank.com",
        domain_type="FQDN",
        root_domain="bank.com",
        source_method="com.bank.NetClient.connect",
        protocol="HTTPS",
    )

    assert dom.domain == "api.bank.com"
    assert dom.root_domain == "bank.com"
    assert dom.domain_type == "FQDN"
