import pytest
from app.services.enterprise_governance.third_party_risk_engine import ThirdPartyRiskEngine

def test_third_party_risk_listing():
    engine = ThirdPartyRiskEngine()
    vendors = engine.list_vendors()
    assert len(vendors) >= 1
    assert vendors[0].criticality == "TIER_1"
