import pytest
from app.services.digital_twin_lab.twin_governance_engine import TwinGovernanceEngine

def test_twin_immutable_sha256_audit_logging():
    gov = TwinGovernanceEngine()
    h1 = gov.log_simulation_audit("SCENARIO_SIMULATED", {"scenario_id": "scen_01"})
    assert len(h1) == 64
    assert len(gov._audit_log) >= 1
