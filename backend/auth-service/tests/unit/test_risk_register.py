import pytest
from app.services.enterprise_governance.enterprise_risk_engine import EnterpriseRiskEngine

def test_risk_register_listing():
    engine = EnterpriseRiskEngine()
    risks = engine.list_risks()
    assert len(risks) >= 1
    assert risks[0].treatment in ("MITIGATE", "ACCEPT", "TRANSFER", "AVOID")
