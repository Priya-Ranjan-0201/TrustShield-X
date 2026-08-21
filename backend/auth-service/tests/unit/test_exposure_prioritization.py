import pytest
from app.services.exposure.exposure_prioritization_engine import ExposurePrioritizationEngine
from app.schemas.exposure_models import AssetDTO


def test_exposure_prioritization_and_severity_ranking():
    engine = ExposurePrioritizationEngine()

    crit_asset = AssetDTO(
        asset_id="ast_crit",
        asset_type="DOMAIN",
        canonical_identifier="prod-db.internal",
        display_identifier="prod-db.internal",
        criticality="CRITICAL",
        tenant_id="tenant_prio",
    )

    finding = engine.create_finding(
        asset=crit_asset,
        title="Critical Database Exposure",
        description="Database port exposed publicly with dropped trust score",
        exposure_score=95.0,
        risk_score=90.0,
        trust_score=40.0,
        tenant_id="tenant_prio",
    )
    assert finding.severity == "CRITICAL"
    assert finding.lifecycle_state == "NEW"

    # Transition finding to TRIAGED
    updated = engine.update_lifecycle(finding.finding_id, "TRIAGED", "tenant_prio")
    assert updated.lifecycle_state == "TRIAGED"
