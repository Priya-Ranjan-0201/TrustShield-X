import pytest
from app.services.knowledge_fabric.cyber_security_knowledge_fabric import CyberSecurityKnowledgeFabric


def test_cyber_security_knowledge_fabric_e2e_lifecycle():
    fabric = CyberSecurityKnowledgeFabric()
    tenant = "tenant_e2e_fabric"

    # 1. Register Objects
    obj1 = fabric.objects.create_object("ASSET", "srv_e2e_host", tenant_id=tenant, confidence=0.95)
    obj2 = fabric.objects.create_object("SERVICE", "svc_e2e_app", tenant_id=tenant, confidence=0.92)
    assert obj1.object_id is not None
    assert obj2.object_id is not None

    # 2. Link with Relationship & Provenance
    rel = fabric.relationships.create_relationship(
        source_id=obj1.object_id,
        target_id=obj2.object_id,
        relation_type="HOSTS",
        evidence=["ev_docker_compose_file"],
        confidence=0.98,
    )
    assert rel.relationship_id is not None

    # 3. Record Temporal Interval
    temp = fabric.temporal.record_temporal_state(obj1.object_id, "CURRENT")
    assert temp.temporal_state == "CURRENT"

    # 4. Evidence Graph Integration
    ev_node = fabric.evidence_graph.add_node("ev_docker_compose_file", "CONFIG_FILE", "Compose Spec", "EVIDENCE")
    fabric.evidence_graph.add_edge("ev_docker_compose_file", obj2.object_id, "SUPPORTS")
    assert ev_node.confidence == 0.90

    # 5. Create Security Assertion & Lineage
    asrt = fabric.assertions.create_assertion(
        statement="E2E Host safely runs E2E App.",
        supporting_evidence=["ev_docker_compose_file"],
        confidence=0.95,
        status="VERIFIED",
    )
    fabric.lineage.record_lineage(
        conclusion_id=asrt.assertion_id,
        created_by_model="E2E_Test_Engine",
        source_data=["config_dump"],
        supporting_evidence=["ev_docker_compose_file"],
        transformations=["PARSE"],
        models_used=["TEST_SUITE"],
    )

    # 6. Query Security Knowledge Assistant
    ans = fabric.assistant.answer_query("Tell me about srv_checkout_production", tenant_id=tenant)
    assert ans.answer != ""
    assert len(ans.evidence) >= 1

    # 7. Get Aggregated Summary
    summary = fabric.get_summary(tenant_id=tenant)
    assert summary.total_knowledge_objects >= 2
    assert summary.overall_quality_score > 85.0
