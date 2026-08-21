"""Unit tests for Wi-Fi Networking Intelligence (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkWifiDTO


def test_wifi_dto():
    wifi = NetworkWifiDTO(
        caller_method="com.bank.Wifi.getSSID",
        wifi_feature="WIFI_MANAGER",
        ssid="[REDACTED_SSID]",
    )

    assert wifi.wifi_feature == "WIFI_MANAGER"
    assert wifi.ssid == "[REDACTED_SSID]"
