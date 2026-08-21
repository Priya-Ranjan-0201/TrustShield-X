import pytest
from app.services.digital_twin_lab.twin_governance_engine import TwinGovernanceEngine

def test_twin_rbac_permissions():
    gov = TwinGovernanceEngine()
    assert gov.check_permission("ADMIN", "twin.admin") is True
    assert gov.check_permission("SOC_ANALYST", "twin.simulate") is True
    assert gov.check_permission("AUDITOR", "twin.simulate") is False
