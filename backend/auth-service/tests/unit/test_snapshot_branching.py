import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_snapshot_branching_isolation():
    engine = DigitalTwinStateEngine()
    branch = engine.create_branch("twstate_v1_prod_sync", "branch_waf_hardening", {"rate_limit": 50})
    assert branch.is_active is True
    assert branch.parent_state_id == "twstate_v1_prod_sync"
