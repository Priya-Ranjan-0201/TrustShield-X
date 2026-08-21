import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_assurance_validated_controls_in_twin():
    engine = DigitalTwinStateEngine()
    state = engine.get_state("twstate_v1_prod_sync")
    validated_controls = [c for c in state.controls if c.get("validated")]
    assert len(validated_controls) >= 2
