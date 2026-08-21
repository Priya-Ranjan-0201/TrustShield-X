import pytest
from app.services.zero_trust_exposure.asset_discovery_inventory_engine import AssetDiscoveryInventoryEngine

def test_unknown_asset_detection():
    engine = AssetDiscoveryInventoryEngine()
    engine.register_approved_asset("ASSET-KNOWN", "t1", "Main Web App", "WEB_APP", "SecOps")
    
    engine.record_discovered_asset("ASSET-KNOWN", "t1", "app.truthshield.io", "WEB_APP")
    engine.record_discovered_asset("ASSET-UNKNOWN-99", "t1", "unapproved-test.truthshield.io", "WEB_APP")
    
    unknowns = engine.detect_unknown_assets("t1")
    assert len(unknowns) == 1
    assert unknowns[0]["asset_id"] == "ASSET-UNKNOWN-99"
    assert unknowns[0]["status"] == "UNKNOWN_EXTERNAL_ASSET"
