import pytest
from app.services.knowledge_fabric.evidence_graph_engine import EvidenceGraphEngine


def test_evidence_corroboration_multiple_supports():
    engine = EvidenceGraphEngine()

    engine.add_node("ev_flow_01", "NETFLOW", "Netflow Record", epistemic_status="EVIDENCE", confidence=0.90)
    engine.add_node("ev_flow_02", "NETFLOW", "Netflow Record", epistemic_status="EVIDENCE", confidence=0.92)

    engine.add_edge("ev_flow_01", "asrt_checkout_at_risk", "SUPPORTS")
    engine.add_edge("ev_flow_02", "asrt_checkout_at_risk", "SUPPORTS")

    supp = engine.get_supporting_evidence("asrt_checkout_at_risk")
    assert len(supp) >= 5
