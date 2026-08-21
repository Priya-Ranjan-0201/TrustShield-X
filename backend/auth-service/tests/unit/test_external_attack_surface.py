import pytest
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine

def test_easm_asset_discovery_and_shadow_it():
    engine = ExternalAttackSurfaceEngine()
    
    # Discover legitimate asset
    a1 = engine.discover_asset(
        asset_id="EXT-1",
        tenant_id="tenant-alpha",
        asset_type="DOMAIN",
        identifier="auth.truthshield.io",
        discovery_method="DNS_SCAN",
        confidence=1.0,
        owner="SecOps"
    )
    assert a1["is_shadow_it"] is False
    
    # Discover unmanaged shadow IT asset
    a2 = engine.discover_asset(
        asset_id="EXT-2",
        tenant_id="tenant-alpha",
        asset_type="STORAGE_BUCKET",
        identifier="dev-unmanaged-test-bucket",
        discovery_method="CERTIFICATE_TRANSPARENCY",
        confidence=0.85,
        owner="UNKNOWN"
    )
    assert a2["is_shadow_it"] is True
    
    shadow_assets = engine.detect_shadow_it("tenant-alpha")
    assert len(shadow_assets) == 1
    assert shadow_assets[0]["asset_id"] == "EXT-2"
