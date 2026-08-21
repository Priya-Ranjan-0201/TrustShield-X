import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_threat_intelligence_ingestion_in_twin():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    assert len(state.threats) >= 1
    assert state.threats[0]["name"] == "AP-44 Campaign"
