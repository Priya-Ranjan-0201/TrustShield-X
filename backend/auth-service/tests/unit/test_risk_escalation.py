import pytest
from app.services.enterprise_governance.enterprise_risk_engine import EnterpriseRiskEngine

def test_risk_escalation_owner():
    engine = EnterpriseRiskEngine()
    risk = engine.list_risks()[0]
    assert risk.owner == "CISO"
