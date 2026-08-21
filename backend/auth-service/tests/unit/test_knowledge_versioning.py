import pytest
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager


def test_knowledge_versioning_and_immutability():
    manager = KnowledgeObjectManager()

    obj = manager.create_object(
        object_type="ASSET",
        canonical_identifier="srv_app_node_1",
        confidence=0.80,
    )
    assert obj.version == 1

    updated = manager.update_object(obj.object_id, new_confidence=0.95, change_reason="EDR_TELEMETRY")
    assert updated.version == 2
    assert updated.confidence == 0.95

    history = manager.get_object_history(obj.object_id)
    assert len(history) == 2
    assert history[0].version == 1
    assert history[0].confidence == 0.80
    assert history[1].version == 2
    assert history[1].confidence == 0.95
