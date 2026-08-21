"""Unit tests for Report Schema DTOs (Phase 4.0 Part 1)."""

import pytest
from app.schemas.digital_trust_report_models import DigitalTrustReportDTO, TrustOverviewDTO, ReportDocumentDTO


def test_report_schema_dto():
    overview = TrustOverviewDTO(risk_score=25.0, risk_band="LOW_RISK")
    doc = ReportDocumentDTO(
        report_id="rep_1",
        analysis_id="an_1",
        generated_at="2026-08-13T20:00:00Z",
        trust_overview=overview,
    )
    dto = DigitalTrustReportDTO(
        report_id="rep_1",
        analysis_id="an_1",
        created_at="2026-08-13T20:00:00Z",
        document=doc,
    )

    assert dto.report_id == "rep_1"
    assert dto.document.trust_overview.risk_score == 25.0
