import pytest
from app.services.zero_trust_exposure.asset_discovery_inventory_engine import AssetDiscoveryInventoryEngine

def test_internal_asset_inventory():
    engine = AssetDiscoveryInventoryEngine()
    
    ast = engine.register_internal_asset(
        asset_id="INT-10",
        tenant_id="tenant-alpha",
        name="Primary PostgreSQL Cluster",
        asset_type="DATABASE",
        environment="PRODUCTION",
        criticality="CRITICAL",
        ip_address="10.0.4.12",
        owner="DataOps"
    )
    assert ast["criticality"] == "CRITICAL"
    assert len(engine.get_assets("tenant-alpha")) == 1
