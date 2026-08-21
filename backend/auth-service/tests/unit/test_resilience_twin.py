import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_resilience_recovery_paths_in_twin():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    assert len(state.recovery_paths) >= 1
    assert state.recovery_paths[0]["id"] == "rec_pg_failover"
