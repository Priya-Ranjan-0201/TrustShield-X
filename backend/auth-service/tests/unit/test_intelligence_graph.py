import pytest
from app.services.federation.federated_trust_graph_engine import FederatedTrustGraphEngine


def test_federated_trust_graph_and_hypotheses():
    engine = FederatedTrustGraphEngine()

    # 1. Add edge
    edge = engine.add_federated_edge("phish-drop.com", "CAMP-2026-0891", relationship="PART_OF", confidence=0.92)
    assert edge["relationship"] == "PART_OF"
    assert edge["confidence"] == 0.92

    # 2. Create actor hypothesis with counter-evidence
    hyp = engine.create_actor_hypothesis(
        actor_label="APT-FIN-STORM",
        supporting_evidence_ids=["ev_c2_dns", "ev_dex_hash"],
        counter_evidence_ids=["ev_diff_compiler_string"],
        confidence=0.75,
    )
    assert hyp.status == "HYPOTHESIS_UNCONFIRMED"
    assert len(hyp.counter_evidence_ids) == 1
    assert len(hyp.alternative_hypotheses) >= 2
