import pytest
from app.services.exposure.asset_inventory_service import AssetInventoryService
from app.services.exposure.asset_baseline_engine import AssetBaselineEngine
from app.services.exposure.change_detection_engine import ChangeDetectionEngine
from app.services.exposure.exposure_scoring_engine import ExposureScoringEngine
from app.services.exposure.exposure_prioritization_engine import ExposurePrioritizationEngine
from app.services.exposure.exposure_alert_correlation_engine import ExposureAlertCorrelationEngine
from app.services.exposure.continuous_monitoring_scheduler import ContinuousMonitoringScheduler
from app.schemas.exposure_models import AssetObservationDTO


def test_full_continuous_exposure_management_core_loop():
    """
    E2E Integration Test of Full Continuous Digital Trust Monitoring & Exposure Management Loop:
    DISCOVER \u2192 IDENTIFY \u2192 BASELINE \u2192 MONITOR \u2192 DETECT CHANGE \u2192 CORRELATE \u2192 ASSESS EXPOSURE \u2192 PRIORITIZE \u2192 ALERT \u2192 REBASELINE
    """
    tenant_id = "tenant_p8_e2e"

    # 1. IDENTIFY & REGISTER ASSET
    inventory = AssetInventoryService()
    asset = inventory.register_asset(
        asset_type="DOMAIN",
        raw_identifier="auth.truthshield.io",
        ownership_status="VERIFIED_OWNER",
        criticality="CRITICAL",
        tenant_id=tenant_id,
    )
    assert asset.canonical_identifier == "auth.truthshield.io"
    assert asset.authorization_status == "AUTHORIZED"

    # 2. ESTABLISH BASELINE
    baseline_engine = AssetBaselineEngine()
    baseline = baseline_engine.establish_baseline(
        asset_id=asset.asset_id,
        dns_records={"A": ["198.51.100.10"]},
        tls_certificate={"fingerprint_sha256": "orig_cert_hash", "issuer": "DigiCert"},
        exposed_ports=[80, 443],
        trust_score=95.0,
        risk_score=10.0,
        exposure_score=25.0,
        tenant_id=tenant_id,
    )
    assert baseline.version == 1

    # 3. SCHEDULE MONITORING JOB
    scheduler = ContinuousMonitoringScheduler()
    job = scheduler.schedule_monitoring_job(asset, mode="PASSIVE", tenant_id=tenant_id)
    assert job["status"] == "SCHEDULED"
    scheduler.transition_job_status(job["job_id"], "RUNNING", tenant_id)

    # 4. INGEST OBSERVATION & DETECT CHANGE
    change_engine = ChangeDetectionEngine()
    observation = AssetObservationDTO(
        observation_id="obs_e2e_01",
        asset_id=asset.asset_id,
        tenant_id=tenant_id,
        source_type="PASSIVE",
        source_name="CANONICAL_MONITOR_WORKER",
        observed_data={
            "dns_records": {"A": ["198.51.100.10"]},
            "tls_certificate": {"fingerprint_sha256": "orig_cert_hash", "issuer": "DigiCert"},
            "exposed_ports": [80, 443, 3389],  # Newly exposed RDP port
            "is_public_facing": True,
        },
        confidence=0.98,
    )
    changes = change_engine.evaluate_observation(observation, baseline)
    assert len(changes) == 1
    assert changes[0].change_type == "NEW_EXPOSED_PORTS_DETECTED"
    assert changes[0].classification == "HIGH_RISK"

    # 5. ASSESS EXPOSURE SCORE
    exp_calc = ExposureScoringEngine.calculate_exposure_score(
        asset=asset,
        baseline=baseline,
        current_observation=observation.observed_data,
        has_active_campaign_link=True,
    )
    assert exp_calc["exposure_score"] >= 80.0

    # 6. PRIORITIZE EXPOSURE FINDING
    prioritization = ExposurePrioritizationEngine()
    finding = prioritization.create_finding(
        asset=asset,
        title="Critical RDP Exposure on Primary Auth Domain",
        description="Public TCP port 3389 observed on critical auth domain with active campaign linkage",
        exposure_score=exp_calc["exposure_score"],
        risk_score=85.0,
        trust_score=60.0,
        change=changes[0],
        campaign_ids=["CAMP-2026-0891"],
        tenant_id=tenant_id,
    )
    assert finding.severity == "CRITICAL"
    assert finding.lifecycle_state == "NEW"

    # 7. CORRELATE EXPOSURE ALERT
    correlation = ExposureAlertCorrelationEngine()
    event = correlation.correlate_findings([finding], tenant_id=tenant_id)
    assert event is not None
    assert event.severity == "CRITICAL"
    assert event.campaign_association == "CAMP-2026-0891"

    # 8. RESOLVE & REBASELINE
    prioritization.update_lifecycle(finding.finding_id, "RESOLVED", tenant_id)
    new_baseline = baseline_engine.establish_baseline(
        asset_id=asset.asset_id,
        dns_records={"A": ["198.51.100.10"]},
        tls_certificate={"fingerprint_sha256": "orig_cert_hash", "issuer": "DigiCert"},
        exposed_ports=[80, 443],  # Remediated: port 3389 closed
        trust_score=95.0,
        risk_score=10.0,
        exposure_score=25.0,
        tenant_id=tenant_id,
    )
    assert new_baseline.version == 2
    assert 3389 not in new_baseline.exposed_ports
