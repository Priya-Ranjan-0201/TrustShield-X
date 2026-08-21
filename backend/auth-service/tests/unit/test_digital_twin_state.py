import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_digital_twin_state_creation_and_fields():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    assert state is not None
    assert state.version == "v1.0.0-PROD-SYNC"
    assert state.freshness_status == "FRESH"
    assert state.confidence_score == 0.98
    assert len(state.assets) >= 3
