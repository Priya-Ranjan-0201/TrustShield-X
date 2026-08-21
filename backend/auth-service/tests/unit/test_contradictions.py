import pytest
from app.services.knowledge_fabric.evidence_contradiction_engine import EvidenceContradictionEngine


def test_contradiction_preservation_and_conflict_state():
    engine = EvidenceContradictionEngine()

    c = engine.record_contradiction(
        entity_id="srv_payment_gateway",
        conflict_type="CLASSIFICATION_DISAGREEMENT",
        evidence_a_id="ev_scanner_a",
        evidence_b_id="ev_scanner_b",
        description="Scanner A reports CVE patched while Scanner B reports vulnerable binary active.",
    )

    assert c.conflict_state == "CONFLICTING"
    assert c.entity_id == "srv_payment_gateway"

    entity_contras = engine.get_contradictions_for_entity("srv_payment_gateway")
    assert len(entity_contras) == 1
