import pytest
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine

def test_external_asset_discovery():
    engine = ExternalAttackSurfaceEngine()
    asset = engine.discover_asset(
        asset_id="EXT-100",
        tenant_id="t1",
        identifier="api.truthshield.io",
        asset_type="DOMAIN",
        open_ports=[80, 443],
        confidence=0.99
    )
    assert asset["asset_id"] == "EXT-100"
    assert asset["confidence"] == 0.99
    assert asset["discovery_method"] == "PASSIVE_DISCOVERY"
