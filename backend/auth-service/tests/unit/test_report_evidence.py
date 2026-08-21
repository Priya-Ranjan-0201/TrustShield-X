"""Unit tests for Report Evidence Cards Generation (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO, ConsolidationResultDTO


def test_report_evidence_cards():
    generator = DigitalTrustReportGenerator()
    findings = [
        CanonicalFindingDTO(
            finding_id="f1",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK_THREAT",
            title="Suspicious Network Endpoint",
            description="Exfiltrating data to external domain",
        )
    ]
    c_dto = ConsolidationResultDTO(findings=findings)

    doc = generator.build_report_document(analysis_id="an_1", consolidation_result_dto=c_dto)

    assert len(doc.evidence_cards) == 1
    assert doc.evidence_cards[0].card_id == "card_f1"
