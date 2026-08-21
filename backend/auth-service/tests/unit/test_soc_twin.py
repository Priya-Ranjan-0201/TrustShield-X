import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_soc_playbook_representation_in_twin():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    assert len(state.playbooks) >= 1
    assert state.playbooks[0]["id"] == "pb_isolate_host"
