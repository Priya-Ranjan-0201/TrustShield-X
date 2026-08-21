"""Unit tests for Report Schema Versioning (Phase 4.0 Part 1)."""

import pytest
from app.schemas.digital_trust_report_models import DigitalTrustReportDTO, ReportDocumentDTO, TrustOverviewDTO


def test_report_versioning_dto():
    overview = TrustOverviewDTO()
    doc = ReportDocumentDTO(
        report_id="r1",
        analysis_id="a1",
        report_version="1.0.0",
        schema_version="4.0.0",
        generated_at="2026-08-13T20:00:00Z",
        trust_overview=overview,
    )
    dto = DigitalTrustReportDTO(
        report_id="r1",
        analysis_id="a1",
        report_version="1.0.0",
        schema_version="4.0.0",
        created_at="2026-08-13T20:00:00Z",
        document=doc,
    )

    assert dto.schema_version == "4.0.0"
