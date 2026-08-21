"""Unit Tests — Report Comparison (Phase 4.0 Part 3 — Section 79)."""

import pytest
from app.services.report_rendering_orchestrator import ReportRenderingOrchestrator
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestReportComparison:
    """Section 79: Test analytical comparison between two report versions."""

    def test_compare_two_reports(self):
        orch = ReportRenderingOrchestrator()
        ov1 = TrustOverviewDTO(risk_score=75.0, risk_band="HIGH_RISK", evidence_count=5)
        f1 = ReportFindingDTO(finding_id="f_old", category="API", title="Old Finding", description="Desc")
        doc1 = ReportDocumentDTO(report_id="rep_1", analysis_id="a1", report_version="1.0.0", generated_at="2026-08-14T00:00:00Z", trust_overview=ov1, major_findings=[f1])

        ov2 = TrustOverviewDTO(risk_score=35.0, risk_band="LOW_RISK", evidence_count=2)
        f2 = ReportFindingDTO(finding_id="f_new", category="NET", title="New Finding", description="Desc")
        doc2 = ReportDocumentDTO(report_id="rep_1", analysis_id="a2", report_version="2.0.0", generated_at="2026-08-14T01:00:00Z", trust_overview=ov2, major_findings=[f2])

        diff = orch.compare_reports(doc1, doc2)
        assert diff.risk_score_delta == -40.0
        assert diff.risk_band_changed is True
        assert diff.risk_band_a == "HIGH_RISK"
        assert diff.risk_band_b == "LOW_RISK"
        assert "f_new" in diff.findings_added
        assert "f_old" in diff.findings_removed
        assert diff.evidence_count_delta == -3
        assert diff.report_version_changed is True
