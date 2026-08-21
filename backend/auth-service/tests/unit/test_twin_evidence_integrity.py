import pytest
from app.services.digital_twin_lab.twin_governance_engine import TwinGovernanceEngine

def test_twin_evidence_hash_chaining():
    gov = TwinGovernanceEngine()
    h1 = gov.log_simulation_audit("ACTION_1", {})
    h2 = gov.log_simulation_audit("ACTION_2", {})
    assert gov._audit_log[-1]["prev_hash"] == h1
    assert h1 != h2
