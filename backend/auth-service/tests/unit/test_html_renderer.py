"""Unit Tests — HTML Report Renderer (Phase 4.0 Part 3 — Section 10)."""

import pytest
from app.services.renderers.html_report_renderer import HTMLReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestHTMLReportRenderer:
    """Test HTML Report rendering structure and content."""

    def test_html_render_structure(self):
        r = HTMLReportRenderer()
        ov = TrustOverviewDTO(risk_score=45.0, risk_band="MODERATE_RISK", confidence="HIGH", evidence_sufficiency="SUFFICIENT")
        f1 = ReportFindingDTO(finding_id="F123", category="NETWORK", title="Suspicious Domain", description="Connected to unusual IP")
        ev1 = ReportEvidenceCardDTO(card_id="E456", title="DNS Query", category="NETWORK", observation="Queried example.com")
        doc = ReportDocumentDTO(
            report_id="rep_html_01",
            analysis_id="an_html_01",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f1],
            evidence_cards=[ev1],
            recommendations=["Review network traffic"],
        )

        out_bytes = r.render(doc)
        assert r.validate_output(out_bytes) is True
        text = out_bytes.decode("utf-8")

        assert "rep_html_01" in text
        assert "45.0" in text
        assert "MODERATE_RISK" in text
        assert "finding-F123" in text
        assert "evidence-E456" in text
        assert "Review network traffic" in text
        assert "<!DOCTYPE html>" in text
        assert "</html>" in text

    def test_html_watermark_option(self):
        r = HTMLReportRenderer()
        ov = TrustOverviewDTO(risk_score=10.0, risk_band="TRUSTED")
        doc = ReportDocumentDTO(report_id="rep_wm", analysis_id="an_wm", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        out_bytes = r.render(doc, options={"watermark": "CONFIDENTIAL"})
        text = out_bytes.decode("utf-8")
        assert "CONFIDENTIAL" in text
