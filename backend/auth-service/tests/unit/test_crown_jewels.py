import pytest
from app.services.zero_trust_exposure.crown_jewel_engine import CrownJewelEngine

def test_crown_jewel_registration():
    engine = CrownJewelEngine()
    jewel = engine.register_crown_jewel(
        jewel_id="JEWEL-HSM-01",
        tenant_id="t1",
        name="Root HSM Master Keystore",
        resource_type="CIPHER_KEYSTORE",
        sensitivity="HIGHLY_RESTRICTED"
    )
    assert jewel["sensitivity"] == "HIGHLY_RESTRICTED"
    assert jewel["blast_radius_factor"] == 3.0
