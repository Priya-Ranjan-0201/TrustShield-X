import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_recovery_what_if_failover():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    rec = state.recovery_paths[0]
    assert rec["id"] == "rec_pg_failover"
    assert rec["rto_seconds"] == 120
