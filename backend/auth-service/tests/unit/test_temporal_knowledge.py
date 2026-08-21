import pytest
from app.services.knowledge_fabric.temporal_knowledge_engine import TemporalKnowledgeEngine


def test_temporal_knowledge_states():
    engine = TemporalKnowledgeEngine()

    engine.record_temporal_state("srv_app_01", temporal_state="HISTORICAL", valid_from="2026-01-01T00:00:00Z")
    engine.record_temporal_state("srv_app_01", temporal_state="CURRENT", valid_from="2026-08-01T00:00:00Z")

    history = engine.get_temporal_history("srv_app_01")
    assert len(history) == 2

    current = engine.get_current_state("srv_app_01")
    assert current is not None
    assert current.temporal_state == "CURRENT"
    assert current.valid_from == "2026-08-01T00:00:00Z"
