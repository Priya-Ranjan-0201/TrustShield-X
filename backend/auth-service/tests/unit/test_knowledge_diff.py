import pytest
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService


def test_knowledge_diff_detection():
    fabric = KnowledgeFabricService()
    # Snapshot A: 1 entity
    obj1 = fabric.register_object("ENTITY", "domain:portal-stage1.com", "tenant_diff", confidence=0.70)
    snap_a = fabric.create_snapshot("Snapshot A", "tenant_diff")

    # Add new evidence and update confidence
    obj2 = fabric.register_object("EVIDENCE", "evid:trojan_payload", "tenant_diff", confidence=0.98)
    fabric.update_object_confidence(obj1.knowledge_object_id, 0.95, "Corroborated", "analyst", "tenant_diff")
    snap_b = fabric.create_snapshot("Snapshot B", "tenant_diff")

    diff = fabric.compute_diff(snap_a.snapshot_id, snap_b.snapshot_id, "tenant_diff")
    assert obj2.knowledge_object_id in diff.new_evidence
    assert len(diff.changed_confidence) >= 1
    assert "new evidence items added" in diff.summary
