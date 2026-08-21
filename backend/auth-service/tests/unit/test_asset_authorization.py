import pytest
from app.services.exposure.asset_inventory_service import AssetInventoryService


def test_asset_authorization_and_ownership_invariants():
    service = AssetInventoryService()

    # Invariant: Claimed owner remains PENDING_VERIFICATION until explicitly verified
    asset = service.register_asset(
        asset_type="DOMAIN",
        raw_identifier="partner-portal.com",
        ownership_status="CLAIMED_OWNER",
        tenant_id="tenant_auth",
    )
    assert asset.authorization_status == "PENDING_VERIFICATION"

    # Explicit verification transition
    verified = service.update_ownership_status(
        asset_id=asset.asset_id,
        new_status="VERIFIED_OWNER",
        tenant_id="tenant_auth",
    )
    assert verified.ownership_status == "VERIFIED_OWNER"
    assert verified.authorization_status == "AUTHORIZED"
