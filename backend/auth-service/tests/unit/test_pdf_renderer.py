"""Unit Tests — PDF Report Renderer (Phase 4.0 Part 3 — Section 29)."""

import pytest
from app.services.renderers.pdf_report_renderer import PDFReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestPDFReportRenderer:
    """Test PDF Report generation binary integrity."""

    def test_pdf_render_valid_binary(self):
        r = PDFReportRenderer()
        ov = TrustOverviewDTO(risk_score=60.0, risk_band="MODERATE_RISK", confidence="HIGH", evidence_sufficiency="SUFFICIENT")
        f = ReportFindingDTO(finding_id="f_pdf", category="MALWARE", title="Trojan Activity", description="Background service execution")
        doc = ReportDocumentDTO(
            report_id="rep_pdf_test",
            analysis_id="an_pdf_test",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            recommendations=["Quarantine application"],
        )

        out_bytes = r.render(doc)
        assert r.validate_output(out_bytes) is True
        assert out_bytes.startswith(b"%PDF-1.")
        assert b"%%EOF" in out_bytes
        assert r.calculate_size(out_bytes) > 100
        assert len(r.calculate_hash(out_bytes)) == 64
