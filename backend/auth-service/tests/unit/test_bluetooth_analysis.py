"""Unit tests for Bluetooth Hardware Networking (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkBluetoothDTO


def test_bluetooth_dto():
    bt = NetworkBluetoothDTO(
        caller_method="com.bank.BLE.scan",
        bluetooth_type="BLE",
        uuid="0000180d-0000-1000-8000-00805f9b34fb",
        operation="SCAN",
    )

    assert bt.bluetooth_type == "BLE"
    assert bt.operation == "SCAN"
