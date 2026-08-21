import pytest
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService


def test_register_and_retrieve_knowledge_object():
    fabric = KnowledgeFabricService()
    obj = fabric.register_object(
        object_type="ENTITY",
        canonical_reference="domain:malicious-c2.net",
        tenant_id="tenant_alpha",
        confidence=0.92,
        classification="RESTRICTED",
    )
    assert obj.knowledge_object_id.startswith("kobj_")
    assert obj.object_type == "ENTITY"
    assert obj.confidence == 0.92

    retrieved = fabric.get_object(obj.knowledge_object_id, "tenant_alpha")
    assert retrieved is not None
    assert retrieved.canonical_reference == "domain:malicious-c2.net"


def test_link_knowledge_objects():
    fabric = KnowledgeFabricService()
    obj1 = fabric.register_object("ENTITY", "apk:sha256_111", "tenant_alpha")
    obj2 = fabric.register_object("CAMPAIGN", "camp:banking_trojan_01", "tenant_alpha")

    rel = fabric.link_objects(
        source_id=obj1.knowledge_object_id,
        target_id=obj2.knowledge_object_id,
        relationship_type="PART_OF",
        confidence=0.95,
        evidence_ids=["evid_dex_01"],
        tenant_id="tenant_alpha",
    )
    assert rel.relationship_type == "PART_OF"
    assert rel.source_id == obj1.knowledge_object_id
    assert rel.target_id == obj2.knowledge_object_id

    rels = fabric.get_object_relationships(obj1.knowledge_object_id, "tenant_alpha")
    assert len(rels) == 1
    assert rels[0].relationship_id == rel.relationship_id


def test_caused_by_downgrade_when_unverified():
    fabric = KnowledgeFabricService()
    obj1 = fabric.register_object("INCIDENT", "inc_001", "tenant_alpha")
    obj2 = fabric.register_object("RESPONSE", "act_001", "tenant_alpha")

    # Invariant: If causality is not verified, CAUSED_BY degrades to ASSOCIATED_WITH
    rel = fabric.link_objects(
        source_id=obj1.knowledge_object_id,
        target_id=obj2.knowledge_object_id,
        relationship_type="CAUSED_BY",
        causality_verified=False,
        tenant_id="tenant_alpha",
    )
    assert rel.relationship_type == "ASSOCIATED_WITH"
