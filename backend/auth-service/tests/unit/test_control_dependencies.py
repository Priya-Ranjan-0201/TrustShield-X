import pytest
from app.services.assurance_fabric.security_control_dependency_graph import SecurityControlDependencyGraph

def test_control_dependencies():
    graph = SecurityControlDependencyGraph()
    affected = graph.get_affected_controls(["app_auth_service"])
    assert "ctl_tenant_isolation" in affected
    assert "ctl_four_eyes_response" in affected
