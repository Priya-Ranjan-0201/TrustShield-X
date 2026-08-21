import pytest
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager


def test_knowledge_freshness_tracking():
    manager = KnowledgeObjectManager()
    objs = manager.list_objects("default_tenant")

    for o in objs:
        assert o.validity_start is not None
        assert o.created_at is not None
