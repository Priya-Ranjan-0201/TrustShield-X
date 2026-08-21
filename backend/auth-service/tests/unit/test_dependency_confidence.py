import pytest
from app.services.resilience_twin.cyber_dependency_graph_engine import CyberDependencyGraphEngine


def test_dependency_confidence_states():
    engine = CyberDependencyGraphEngine()
    dep = engine.add_dependency(
        source_id="service_analytics",
        target_id="queue_kafka_events",
        relation_type="SERVICE_DEPENDS_ON",
        confidence_state="INFERRED",
        confidence_score=0.65,
    )

    assert dep.confidence_state == "INFERRED"
    assert dep.confidence_score == 0.65

    graph = engine.build_graph()
    assert graph.unverified_count >= 1
