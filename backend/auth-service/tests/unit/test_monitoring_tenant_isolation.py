import pytest
from app.services.exposure.asset_inventory_service import AssetInventoryService
from app.services.exposure.exposure_prioritization_engine import ExposurePrioritizationEngine


def test_asset_inventory_tenant_isolation():
    service = AssetInventoryService()

    # Register asset under Tenant Alpha
    a_alpha = service.register_asset(
        asset_type="DOMAIN",
        raw_identifier="confidential-alpha.io",
        tenant_id="tenant_alpha",
    )

    # Tenant Alpha can retrieve
    assert service.get_asset(a_alpha.asset_id, "tenant_alpha") is not None

    # Tenant Beta cannot retrieve Tenant Alpha's asset
    assert service.get_asset(a_alpha.asset_id, "tenant_beta") is None


def test_exposure_findings_tenant_isolation():
    engine = ExposurePrioritizationEngine()
    inventory = AssetInventoryService()

    asset_a = inventory.register_asset(
        asset_type="DOMAIN",
        raw_identifier="app-alpha.io",
        tenant_id="tenant_alpha",
    )

    finding_a = engine.create_finding(
        asset=asset_a,
        title="Alpha Vulnerability",
        description="Confidential finding for tenant Alpha",
        exposure_score=80.0,
        risk_score=70.0,
        trust_score=50.0,
        tenant_id="tenant_alpha",
    )

    # Tenant Alpha sees finding
    findings_alpha = engine.list_findings("tenant_alpha")
    assert len(findings_alpha) == 1

    # Tenant Beta sees 0 findings
    findings_beta = engine.list_findings("tenant_beta")
    assert len(findings_beta) == 0
