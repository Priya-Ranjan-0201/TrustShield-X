import pytest
from app.services.zero_trust_exposure.crown_jewel_engine import CrownJewelEngine

def test_crown_jewel_protection():
    engine = CrownJewelEngine()
    
    cj = engine.register_crown_jewel(
        jewel_id="CJ-01",
        tenant_id="tenant-alpha",
        name="Customer PII Vault",
        data_classification="RESTRICTED",
        recovery_time_objective_hours=1,
        loss_impact_financial="CRITICAL",
        zone_id="Z-VAULT"
    )
    assert cj["protection_level"] == "MAXIMUM_ZERO_TRUST"
    assert len(engine.get_crown_jewels("tenant-alpha")) == 1
