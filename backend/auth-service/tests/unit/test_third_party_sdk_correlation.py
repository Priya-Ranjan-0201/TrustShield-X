"""Unit tests for Third-Party SDK Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import ThirdPartyBehaviorDTO


def test_third_party_sdk_dto():
    tp = ThirdPartyBehaviorDTO(
        sdk_name="Google Firebase Analytics",
        sdk_category="ANALYTICS",
        data_collected="App Telemetry",
        network_endpoint="https://app-measurement.com/a",
    )

    assert tp.sdk_name == "Google Firebase Analytics"
    assert tp.sdk_category == "ANALYTICS"
