import pytest
from app.services.digital_twin_lab.business_impact_engine import BusinessImpactEngine

def test_cascade_failure_identification():
    engine = BusinessImpactEngine()
    impact = engine.simulate_business_impact("scen_phishing_lateral_movement", affected_services=["srv_auth"])
    assert len(impact.cascade_failures) >= 1
