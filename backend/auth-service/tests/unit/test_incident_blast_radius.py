import pytest
from app.services.soc.incident_blast_radius_engine import IncidentBlastRadiusEngine


def test_incident_blast_radius_observed_vs_potential():
    engine = IncidentBlastRadiusEngine()
    deps = {
        "srv_checkout": ["srv_payment_gateway", "db_primary_users"],
        "srv_payment_gateway": ["srv_fraud_scoring"],
    }
    br = engine.evaluate_blast_radius("inc_blast_01", ["srv_checkout"], deps)

    assert "srv_checkout" in br.observed_impact_assets
    assert "srv_payment_gateway" in br.potential_impact_assets
    assert "db_primary_users" in br.potential_impact_assets
    assert br.blast_radius_score > 20.0
