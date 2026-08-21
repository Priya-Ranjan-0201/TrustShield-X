"""Unit tests for VPN Service Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkVpnDTO


def test_vpn_dto():
    vpn = NetworkVpnDTO(
        caller_method="com.bank.VPN.startTunnel",
        vpn_service="android.net.VpnService",
        tunnel_config="TUN_INTERFACE",
    )

    assert vpn.vpn_service == "android.net.VpnService"
    assert vpn.tunnel_config == "TUN_INTERFACE"
