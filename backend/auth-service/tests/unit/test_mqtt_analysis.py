"""Unit tests for MQTT Broker Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkMqttDTO


def test_mqtt_dto():
    mqtt = NetworkMqttDTO(
        caller_method="com.bank.IoT.connect",
        broker_url="ssl://mqtt.bank.com",
        port=8883,
        topic="alerts/security",
        qos=1,
    )

    assert mqtt.broker_url == "ssl://mqtt.bank.com"
    assert mqtt.topic == "alerts/security"
    assert mqtt.qos == 1
