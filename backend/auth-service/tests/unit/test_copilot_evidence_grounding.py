import pytest
from app.services.copilot.copilot_evidence_grounder import CopilotEvidenceGrounder


def test_copilot_evidence_grounding_contract():
    grounder = CopilotEvidenceGrounder()
    cit = grounder.create_citation("ev_flow_01", "NETFLOW", "srv_checkout", "Outbound beaconing to IP 198.51.100.42", 0.95)

    ans = grounder.format_answer(
        answer="Checkout service exhibits C2 beaconing.",
        citations=[cit],
        confidence=0.92,
        sources=["NETFLOW_SENSOR"],
        epistemic_status="VERIFIED",
    )

    assert ans.epistemic_status == "VERIFIED"
    assert len(ans.evidence) == 1
    assert ans.evidence[0].evidence_id == "ev_flow_01"
    assert ans.confidence == 0.92
