import pytest
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager


def test_knowledge_objects_creation_and_hashing():
    manager = KnowledgeObjectManager()

    obj = manager.create_object(
        object_type="VULNERABILITY",
        canonical_identifier="CVE-2026-1049",
        tenant_id="tenant_alpha",
        confidence=0.92,
    )

    assert obj.object_id.startswith("kobj_")
    assert obj.object_type == "VULNERABILITY"
    assert len(obj.content_hash) == 64
    assert obj.tenant_id == "tenant_alpha"

    fetched = manager.get_object(obj.object_id, "tenant_alpha")
    assert fetched is not None
    assert fetched.canonical_identifier == "CVE-2026-1049"
