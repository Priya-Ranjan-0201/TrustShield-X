import pytest
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager


def test_knowledge_security_content_hash_integrity():
    manager = KnowledgeObjectManager()
    obj = manager.create_object("HASH", "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3", tenant_id="tenant_sec")

    assert len(obj.content_hash) == 64
    assert obj.object_type == "HASH"
