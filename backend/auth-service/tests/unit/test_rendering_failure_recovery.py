"""Unit Tests — Rendering Failure Recovery (Phase 4.0 Part 3 — Section 84, Tests 23, 24, 25 & Section 88)."""

import pytest
from app.services.report_rendering_engine import ReportRenderingEngine
from app.services.report_rendering_orchestrator import ReportRenderingOrchestrator
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO


class TestRenderingFailureRecovery:
    """Mandatory Tests 23, 24, 25: Missing risk assessment, partial reports, and renderer failure handling."""

    def test_missing_report_doc_fails_safely(self):
        orch = ReportRenderingOrchestrator()
        with pytest.raises(ValueError, match="Missing ReportDocument"):
            orch.render_and_store(report_doc=None)

    def test_unsupported_format_fails_safely(self):
        engine = ReportRenderingEngine()
        ov = TrustOverviewDTO(risk_score=20.0, risk_band="LOW_RISK")
        doc = ReportDocumentDTO(report_id="r1", analysis_id="a1", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        with pytest.raises(ValueError, match="TSX-REPORT-606: Unsupported rendering format"):
            engine.render_artifact(doc, format_name="UNSUPPORTED_XYZ")

    def test_insufficient_evidence_status_preserved(self):
        engine = ReportRenderingEngine()
        ov = TrustOverviewDTO(risk_score=0.0, risk_band="UNKNOWN", confidence="LOW", evidence_sufficiency="INSUFFICIENT")
        doc = ReportDocumentDTO(report_id="r_insuff", analysis_id="a1", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        art, html_b = engine.render_artifact(doc, format_name="HTML")
        assert "INSUFFICIENT" in html_b.decode("utf-8")
