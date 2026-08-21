import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_twin_dependency_graph_topology():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    assert len(state.dependencies) >= 2
    assert state.dependencies[0]["source"] == "ast_api_gw"
