"""Unit tests for Report REST APIs (Phase 4.0 Part 1)."""

import pytest
from app.schemas.envelope import ResponseEnvelope
from app.schemas.digital_trust_report_models import DigitalTrustReportDTO, ReportDocumentDTO, TrustOverviewDTO


def test_report_api_envelope():
    overview = TrustOverviewDTO()
    doc = ReportDocumentDTO(
        report_id="r1",
        analysis_id="a1",
        generated_at="2026-08-13T20:00:00Z",
        trust_overview=overview,
    )
    dto = DigitalTrustReportDTO(
        report_id="r1",
        analysis_id="a1",
        created_at="2026-08-13T20:00:00Z",
        document=doc,
    )

    env = ResponseEnvelope(message="Success", data=dto)
    assert env.success is True
    assert env.data.report_id == "r1"
