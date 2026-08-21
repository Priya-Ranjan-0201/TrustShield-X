import pytest
from app.services.digital_twin_lab.twin_governance_engine import TwinGovernanceEngine

def test_twin_abac_scope_eval():
    gov = TwinGovernanceEngine()
    assert gov.check_permission("CISO", "twin.export") is True
