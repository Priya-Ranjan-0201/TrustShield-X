import pytest
from app.services.resilience.resilience_dependency_graph_engine import ResilienceDependencyGraphEngine
from app.services.resilience_twin.cyber_dependency_graph_engine import CyberDependencyGraphEngine

def test_phase23_resilience_dependency_graph():
    engine = ResilienceDependencyGraphEngine()
    graph = engine.build_graph()
    assert len(graph.nodes) > 0
    assert len(graph.edges) > 0
    assert "ast_pg_primary" in graph.single_points_of_failure

def test_cyber_dependency_graph_building():
    engine = CyberDependencyGraphEngine()
    engine.add_dependency(
        source_id="app_checkout",
        target_id="db_postgres_orders",
        relation_type="DATA_STORED_ON",
        confidence_state="VERIFIED",
    )
    graph = engine.build_graph()
    assert graph.total_dependencies >= 5
