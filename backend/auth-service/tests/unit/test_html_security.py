"""Unit Tests — HTML Security & Sanitization (Phase 4.0 Part 3 — Section 11)."""

import pytest
from app.services.renderers.html_report_renderer import HTMLReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestHTMLSecurity:
    """Section 11: Protect against XSS, script injection, and template injection in HTML."""

    def test_no_external_scripts_or_tracking(self):
        r = HTMLReportRenderer()
        ov = TrustOverviewDTO(risk_score=20.0, risk_band="LOW_RISK")
        doc = ReportDocumentDTO(report_id="rep_sec_html", analysis_id="an_sec", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        out_bytes = r.render(doc)
        text = out_bytes.decode("utf-8")

        # Zero external scripts or tracking
        assert "<script src=" not in text
        assert "http://" not in text or "http://www.w3.org" in text or "https://" in text
        assert "google-analytics" not in text
        assert "fonts.googleapis.com" not in text

    def test_script_tag_in_report_id_escaped(self):
        r = HTMLReportRenderer()
        ov = TrustOverviewDTO(risk_score=20.0, risk_band="LOW_RISK")
        doc = ReportDocumentDTO(report_id="<script>alert(1)</script>", analysis_id="an", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        out_bytes = r.render(doc)
        text = out_bytes.decode("utf-8")

        assert "<script>alert(1)</script>" not in text
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in text
