import pytest
from app.services.exposure.asset_discovery_engine import AssetDiscoveryEngine
from app.services.exposure.asset_inventory_service import AssetInventoryService


def test_shadow_asset_discovery_and_listing():
    inventory = AssetInventoryService()
    discovery = AssetDiscoveryEngine(inventory)

    sh1 = discovery.discover_candidate(
        raw_identifier="corp-vpn.truthshield.io",
        asset_type="DOMAIN",
        discovery_source="PASSIVE_DNS",
        related_brand_or_domain="truthshield",
        confidence=0.85,
        tenant_id="tenant_shd",
    )
    assert sh1.shadow_status == "PROBABLE_SHADOW_ASSET"

    shadows = discovery.list_shadow_assets("tenant_shd")
    assert len(shadows) == 1
    assert shadows[0].canonical_identifier == "corp-vpn.truthshield.io"
