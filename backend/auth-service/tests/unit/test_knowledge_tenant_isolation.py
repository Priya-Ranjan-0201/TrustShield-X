import pytest
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager


def test_knowledge_tenant_isolation():
    manager = KnowledgeObjectManager()

    obj_a = manager.create_object("ASSET", "srv_ten_a", tenant_id="tenant_a")
    obj_b = manager.create_object("ASSET", "srv_ten_b", tenant_id="tenant_b")

    assert manager.get_object(obj_a.object_id, "tenant_a") is not None
    assert manager.get_object(obj_a.object_id, "tenant_b") is None

    list_a = manager.list_objects("tenant_a")
    list_b = manager.list_objects("tenant_b")

    assert any(o.object_id == obj_a.object_id for o in list_a)
    assert not any(o.object_id == obj_a.object_id for o in list_b)
