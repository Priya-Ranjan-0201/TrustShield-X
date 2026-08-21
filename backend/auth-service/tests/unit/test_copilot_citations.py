import pytest
from app.services.copilot.copilot_evidence_grounder import CopilotEvidenceGrounder


def test_copilot_citations_traceability():
    grounder = CopilotEvidenceGrounder()
    cit = grounder.create_citation(
        evidence_id="ev_trivy_99",
        source_id="TRIVY_SCANNER",
        object_id="cve_2026_9942",
        snippet="CVSS 9.8 critical vulnerability in libpayment.so",
        confidence=0.98,
    )

    assert cit.evidence_id == "ev_trivy_99"
    assert cit.source_id == "TRIVY_SCANNER"
    assert cit.object_id == "cve_2026_9942"
    assert cit.timestamp is not None
