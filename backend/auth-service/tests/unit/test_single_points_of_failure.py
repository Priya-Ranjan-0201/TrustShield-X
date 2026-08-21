import pytest
from app.services.resilience_twin.cyber_dependency_graph_engine import CyberDependencyGraphEngine
from app.services.resilience_twin.single_point_of_failure_engine import SinglePointOfFailureEngine


def test_single_point_of_failure_identification():
    dep_engine = CyberDependencyGraphEngine()
    spof_engine = SinglePointOfFailureEngine(dep_engine)

    spofs = spof_engine.identify_spofs()
    assert len(spofs) >= 1

    auth_spof = next((s for s in spofs if s.resource_id == "service_auth_jwt" or s.resource_id == "service_api_gateway"), None)
    assert auth_spof is not None
    assert auth_spof.is_spof is True
    assert len(auth_spof.cascading_affected_services) >= 1
