import pytest
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService


def test_knowledge_snapshot_creation_and_retrieval():
    fabric = KnowledgeFabricService()
    fabric.register_object("ENTITY", "ip:198.51.100.44", "tenant_snap")
    fabric.register_object("EVIDENCE", "evid:cert_sha256", "tenant_snap")

    snapshot = fabric.create_snapshot("August 15 Baseline", "tenant_snap")
    assert snapshot.snapshot_id.startswith("ksnap_")
    assert snapshot.object_count == 2
    assert snapshot.label == "August 15 Baseline"

    retrieved = fabric.get_snapshot(snapshot.snapshot_id, "tenant_snap")
    assert retrieved is not None
    assert retrieved.object_count == 2
