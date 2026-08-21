"""Unit tests for IP Address Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkIPDTO


def test_ip_dto():
    ip = NetworkIPDTO(
        ip_address="192.168.1.1",
        ip_version="IPv4",
        is_private=True,
        is_loopback=False,
        source_method="com.bank.Net.connect",
    )

    assert ip.ip_address == "192.168.1.1"
    assert ip.is_private is True
    assert ip.ip_version == "IPv4"
