import pytest
from app.services.digital_twin_lab.cyber_defense_digital_twin_engine import CyberDefenseDigitalTwinEngine

def test_copilot_twin_query_synthesis():
    engine = CyberDefenseDigitalTwinEngine()
    overview = engine.get_digital_twin_overview("default_tenant")
    assert overview["twin_freshness_status"] == "FRESH"
    assert overview["simulation_accuracy_score"] == 0.96
