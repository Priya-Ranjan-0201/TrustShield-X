import pytest
from app.services.exposure.asset_inventory_service import AssetInventoryService


def test_asset_registration_and_retrieval():
    service = AssetInventoryService()
    asset = service.register_asset(
        asset_type="DOMAIN",
        raw_identifier="AUTH.TRUTHSHIELD.IO.",
        ownership_status="VERIFIED_OWNER",
        criticality="CRITICAL",
        tenant_id="tenant_inv",
    )
    assert asset.asset_id.startswith("ast_")
    assert asset.canonical_identifier == "auth.truthshield.io"
    assert asset.ownership_status == "VERIFIED_OWNER"
    assert asset.authorization_status == "AUTHORIZED"
    assert asset.criticality == "CRITICAL"

    retrieved = service.get_asset(asset.asset_id, "tenant_inv")
    assert retrieved is not None
    assert retrieved.canonical_identifier == "auth.truthshield.io"


def test_asset_score_updates():
    service = AssetInventoryService()
    asset = service.register_asset(
        asset_type="API_ENDPOINT",
        raw_identifier="https://api.truthshield.io/v1/scan",
        tenant_id="tenant_inv",
    )
    updated = service.update_scores(
        asset_id=asset.asset_id,
        exposure_score=65.0,
        trust_score=92.0,
        risk_score=18.0,
        tenant_id="tenant_inv",
    )
    assert updated.exposure_score == 65.0
    assert updated.trust_score == 92.0
    assert updated.risk_score == 18.0
