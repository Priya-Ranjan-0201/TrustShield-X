import pytest
from app.services.cyber_digital_twin.what_if_simulation_engine import WhatIfSimulationEngine

def test_control_gap_detection():
    engine = WhatIfSimulationEngine()
    # Missing MFA, EDR, and Microsegmentation
    gaps = engine.detect_control_gaps("t1", "PUBLIC-SERVER", active_controls=["FIREWALL"])
    assert len(gaps) == 3
    assert all(g["finding"] == "CONTROL_GAP" for g in gaps)
