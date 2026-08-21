import pytest
from app.services.soc.incident_blast_radius_engine import IncidentBlastRadiusEngine


def test_knowledge_enrichment_dependency_topology():
    engine = IncidentBlastRadiusEngine()
    deps = {"srv_auth": ["db_auth_users", "srv_session_cache"]}
    br = engine.evaluate_blast_radius("inc_kn_01", ["srv_auth"], deps)

    assert "db_auth_users" in br.potential_impact_assets
    assert "srv_session_cache" in br.potential_impact_assets
