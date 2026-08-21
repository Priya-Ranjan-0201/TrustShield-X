import pytest
from app.services.cyber_digital_twin.cyber_digital_twin_engine import CyberDigitalTwinEngine

def test_fidelity_gap_detection():
    engine = CyberDigitalTwinEngine()
    # Missing vulnerability and control data triggers gaps
    engine.create_environment("ENV-GAP", "t1", initial_state={"assets": [{"id": "A1"}]})
    fid = engine.calculate_fidelity("ENV-GAP", "t1")
    assert len(fid["fidelity_gaps"]) >= 1
    assert fid["fidelity_gaps"][0]["gap_type"] == "DIGITAL_TWIN_FIDELITY_GAP"
