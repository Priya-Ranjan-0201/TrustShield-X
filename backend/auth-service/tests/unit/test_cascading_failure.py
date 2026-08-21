import pytest
from app.services.resilience_twin.cyber_dependency_graph_engine import CyberDependencyGraphEngine
from app.services.resilience_twin.single_point_of_failure_engine import SinglePointOfFailureEngine


def test_cascading_failure_simulation():
    dep_engine = CyberDependencyGraphEngine()
    spof_engine = SinglePointOfFailureEngine(dep_engine)

    res = spof_engine.model_cascading_failure("service_auth_jwt")
    assert res["initial_failed_node"] == "service_auth_jwt"
    assert res["is_simulated"] is True
    assert "affected_services" in res
