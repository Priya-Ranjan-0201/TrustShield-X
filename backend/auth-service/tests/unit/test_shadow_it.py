import pytest
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine

def test_shadow_it_detection():
    engine = ExternalAttackSurfaceEngine()
    engine.register_public_asset("ASSET-MGT", "t1", "portal.truthshield.io", is_managed=True)
    engine.register_public_asset("ASSET-SHADOW", "t1", "shadow-saas.external.cloud", is_managed=False)
    
    shadow_assets = engine.detect_shadow_it("t1")
    assert len(shadow_assets) == 1
    assert shadow_assets[0]["asset_id"] == "ASSET-SHADOW"
