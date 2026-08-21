import pytest
from app.services.exposure.continuous_monitoring_scheduler import ContinuousMonitoringScheduler
from app.schemas.exposure_models import AssetDTO


def test_monitoring_job_idempotency():
    scheduler = ContinuousMonitoringScheduler()
    asset = AssetDTO(
        asset_id="ast_idem_01",
        asset_type="DOMAIN",
        canonical_identifier="idempotent.example.com",
        display_identifier="idempotent.example.com",
    )

    # First schedule call creates job
    j1 = scheduler.schedule_monitoring_job(asset, mode="PASSIVE", tenant_id="tenant_idem")

    # Second schedule call while first is active returns identical job_id
    j2 = scheduler.schedule_monitoring_job(asset, mode="PASSIVE", tenant_id="tenant_idem")
    assert j1["job_id"] == j2["job_id"]
