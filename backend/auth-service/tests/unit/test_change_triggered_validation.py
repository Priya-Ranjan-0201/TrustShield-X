import pytest
from app.services.assurance_fabric.security_control_dependency_graph import SecurityControlDependencyGraph

def test_change_triggered_validation():
    graph = SecurityControlDependencyGraph()
    affected = graph.get_affected_controls(["db_postgres_cluster"])
    assert "ctl_immutable_audit" in affected
