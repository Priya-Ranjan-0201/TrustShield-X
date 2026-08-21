"""Unit tests for Report JSON Determinism (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO, ConsolidationResultDTO


def test_report_json_determinism():
    generator = DigitalTrustReportGenerator()
    findings = [
        CanonicalFindingDTO(
            finding_id="f2",
            finding_type="TYPE_B",
            finding_category="CAT_B",
            title="B",
            description="Desc B",
        ),
        CanonicalFindingDTO(
            finding_id="f1",
            finding_type="TYPE_A",
            finding_category="CAT_A",
            title="A",
            description="Desc A",
        ),
    ]
    c_dto = ConsolidationResultDTO(findings=findings)

    doc = generator.build_report_document(analysis_id="an_1", consolidation_result_dto=c_dto)

    # Findings should be deterministically sorted by finding_id
    assert doc.major_findings[0].finding_id == "f1"
    assert doc.major_findings[1].finding_id == "f2"
