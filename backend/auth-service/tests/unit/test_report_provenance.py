"""Unit tests for Report Provenance Traceability (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO, ConsolidationResultDTO


def test_report_provenance_links():
    generator = DigitalTrustReportGenerator()
    findings = [
        CanonicalFindingDTO(
            finding_id="f1",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK_THREAT",
            title="Title",
            description="Description",
        )
    ]
    c_dto = ConsolidationResultDTO(findings=findings)

    doc = generator.build_report_document(analysis_id="an_1", consolidation_result_dto=c_dto)

    assert len(doc.provenance) == 1
    assert doc.provenance[0].finding_id == "f1"
