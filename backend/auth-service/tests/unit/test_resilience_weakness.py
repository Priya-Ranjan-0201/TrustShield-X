import pytest
from app.services.resilience_twin.single_point_of_failure_engine import SinglePointOfFailureEngine
from app.services.resilience_twin.cyber_dependency_graph_engine import CyberDependencyGraphEngine


def test_resilience_weakness_concentration_detection():
    dep_engine = CyberDependencyGraphEngine()
    spof_engine = SinglePointOfFailureEngine(dep_engine)

    spofs = spof_engine.identify_spofs()
    assert len(spofs) >= 1
    assert all(s.impact_severity in ("HIGH", "CRITICAL") for s in spofs)
