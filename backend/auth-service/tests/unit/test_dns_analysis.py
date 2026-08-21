"""Unit tests for DNS Resolution Intelligence (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkDNSDTO


def test_dns_dto():
    dns = NetworkDNSDTO(
        caller_method="com.bank.DNS.resolve",
        domain="dns.bank.com",
        resolution_method="InetAddress.getByName",
        is_doh=True,
    )

    assert dns.domain == "dns.bank.com"
    assert dns.is_doh is True
