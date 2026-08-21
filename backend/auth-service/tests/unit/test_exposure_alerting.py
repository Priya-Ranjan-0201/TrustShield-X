import pytest
from app.services.exposure.exposure_alert_correlation_engine import ExposureAlertCorrelationEngine
from app.schemas.exposure_models import ExposureFindingDTO


def test_exposure_alert_correlation_and_cooldown_deduplication():
    engine = ExposureAlertCorrelationEngine(cooldown_minutes=60)

    f1 = ExposureFindingDTO(
        finding_id="fnd_01",
        asset_id="ast_01",
        tenant_id="tenant_alert",
        title="Port 22 Opened",
        description="SSH port exposed",
        severity="HIGH",
        exposure_score=75.0,
        risk_score=70.0,
        trust_score=60.0,
        campaign_ids=["CAMP-2026-0891"],
        recommended_action="Close port",
    )
    f2 = ExposureFindingDTO(
        finding_id="fnd_02",
        asset_id="ast_02",
        tenant_id="tenant_alert",
        title="Suspicious DNS Record",
        description="DNS pointed to rogue IP",
        severity="CRITICAL",
        exposure_score=85.0,
        risk_score=80.0,
        trust_score=40.0,
        campaign_ids=["CAMP-2026-0891"],
        recommended_action="Revert DNS",
    )

    # 1. Correlate batch of 2 related findings into ONE unified event
    event = engine.correlate_findings([f1, f2], tenant_id="tenant_alert")
    assert event is not None
    assert event.event_id.startswith("cexp_")
    assert event.severity == "CRITICAL"
    assert event.campaign_association == "CAMP-2026-0891"
    assert len(event.affected_assets) == 2

    # 2. Immediate duplicate batch should be suppressed due to active cooldown
    dup_event = engine.correlate_findings([f1, f2], tenant_id="tenant_alert")
    assert dup_event is None
