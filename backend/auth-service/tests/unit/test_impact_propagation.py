import pytest
from app.services.digital_twin_lab.business_impact_engine import BusinessImpactEngine

def test_impact_propagation_across_dependencies():
    engine = BusinessImpactEngine()
    impact = engine.simulate_business_impact("scen_phishing_lateral_movement", affected_services=["srv_auth"])
    assert "srv_reports_export" in impact.cascade_failures
