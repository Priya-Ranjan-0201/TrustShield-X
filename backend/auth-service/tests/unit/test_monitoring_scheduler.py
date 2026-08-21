import pytest
from app.services.exposure.continuous_monitoring_scheduler import ContinuousMonitoringScheduler
from app.schemas.exposure_models import AssetDTO


def test_monitoring_job_lifecycle_state_machine():
    scheduler = ContinuousMonitoringScheduler()
    asset = AssetDTO(
        asset_id="ast_sched_01",
        asset_type="DOMAIN",
        canonical_identifier="portal.example.com",
        display_identifier="portal.example.com",
    )

    # 1. Schedule job (CONFIGURED/SCHEDULED)
    job = scheduler.schedule_monitoring_job(asset, mode="PASSIVE", tenant_id="tenant_sched")
    assert job["status"] == "SCHEDULED"

    # 2. RUNNING transition
    job_running = scheduler.transition_job_status(job["job_id"], "RUNNING", "tenant_sched")
    assert job_running["status"] == "RUNNING"

    # 3. COMPLETED transition
    job_completed = scheduler.transition_job_status(job["job_id"], "COMPLETED", "tenant_sched")
    assert job_completed["status"] == "COMPLETED"


def test_monitoring_invalid_transition_fails():
    scheduler = ContinuousMonitoringScheduler()
    asset = AssetDTO(
        asset_id="ast_sched_02",
        asset_type="DOMAIN",
        canonical_identifier="app.example.com",
        display_identifier="app.example.com",
    )
    job = scheduler.schedule_monitoring_job(asset, mode="PASSIVE", tenant_id="tenant_sched")

    # Invariant: Cannot jump from SCHEDULED directly to COMPLETED without RUNNING
    with pytest.raises(ValueError):
        scheduler.transition_job_status(job["job_id"], "COMPLETED", "tenant_sched")
