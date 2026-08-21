import pytest
from app.services.enterprise_governance.third_party_risk_engine import ThirdPartyRiskEngine

def test_vendor_risk_tier():
    engine = ThirdPartyRiskEngine()
    v = engine.list_vendors()[0]
    assert v.risk_level in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
