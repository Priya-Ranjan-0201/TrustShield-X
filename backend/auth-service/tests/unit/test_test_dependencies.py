import pytest
from app.services.assurance.control_dependency_graph_engine import ControlDependencyGraphEngine


def test_control_dependencies():
    engine = ControlDependencyGraphEngine()

    db_deps = engine.get_dependencies("ctrl_db_core")
    assert "ctrl_audit_01" in db_deps
    assert "ctrl_iso_01" in db_deps

    spofs = engine.identify_single_points_of_failure()
    assert len(spofs) >= 1
    assert spofs[0]["critical_component"] == "ctrl_db_core"
