import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_twin_confidence_scoring():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    assert state.confidence_score >= 0.95
