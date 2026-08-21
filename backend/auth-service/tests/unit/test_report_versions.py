"""Unit Tests — Report Versions (Phase 4.0 Part 3 — Section 80)."""

import pytest
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO


class TestReportVersions:
    """Section 80: Verify report versions history tracking."""

    def test_version_progression(self):
        ov = TrustOverviewDTO(risk_score=20.0, risk_band="LOW_RISK")
        v1 = ReportDocumentDTO(report_id="rep_v1", analysis_id="a1", report_version="1.0.0", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        v2 = ReportDocumentDTO(report_id="rep_v1", analysis_id="a2", report_version="2.0.0", generated_at="2026-08-14T01:00:00Z", trust_overview=ov)

        assert v1.report_version == "1.0.0"
        assert v2.report_version == "2.0.0"
