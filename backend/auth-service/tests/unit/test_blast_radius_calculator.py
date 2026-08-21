import pytest
from app.services.zero_trust_exposure.blast_radius_calculator_engine import BlastRadiusCalculatorEngine

def test_blast_radius_calculation():
    engine = BlastRadiusCalculatorEngine()
    
    res = engine.calculate_blast_radius(
        radius_id="BLAST-01",
        tenant_id="tenant-alpha",
        compromised_asset_id="APP-PROD",
        directly_connected_assets=["DB-VAULT", "STORAGE-PROD", "CACHE-NODE"],
        reachable_identities=["alice@tenant-alpha.com", "bob@tenant-alpha.com"],
        downstream_services=["billing-api", "user-api"]
    )
    assert res["impact_scope"] in ["HIGH", "CRITICAL"]
    assert res["containment_recommended"] is True
