import pytest
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService


def test_twin_snapshot_synthetic_credentials():
    service = DigitalSecurityTwinService()

    twin = service.create_twin_from_snapshot(
        source_snapshot_id="snap_corp_master",
        raw_assets=[{"service": "PaymentGateway", "api_key": "live_sk_secret_123"}],
    )

    assert "live_sk_secret_123" not in str(twin.modeled_assets)
    assert twin.source_snapshot_id == "snap_corp_master"
