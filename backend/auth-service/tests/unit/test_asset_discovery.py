import pytest
from app.services.exposure.asset_discovery_engine import AssetDiscoveryEngine
from app.services.exposure.asset_inventory_service import AssetInventoryService


def test_asset_discovery_and_shadow_classification():
    inventory = AssetInventoryService()
    discovery = AssetDiscoveryEngine(inventory)

    # Candidate related to declared brand name but not in declared inventory
    shadow = discovery.discover_candidate(
        raw_identifier="dev-login.truthshield.io",
        asset_type="DOMAIN",
        discovery_source="CERTIFICATE_TRANSPARENCY_LOGS",
        related_brand_or_domain="truthshield",
        confidence=0.88,
        tenant_id="tenant_disc",
    )
    assert shadow.shadow_id.startswith("shd_")
    assert shadow.shadow_status == "PROBABLE_SHADOW_ASSET"
    assert shadow.canonical_identifier == "dev-login.truthshield.io"
