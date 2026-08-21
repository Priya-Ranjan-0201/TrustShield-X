"""Unit Tests — Base Renderer Interface (Phase 4.0 Part 3 — Section 83)."""

import pytest
from app.services.renderers.base_renderer import BaseReportRenderer
from app.services.renderers.json_report_renderer import JSONReportRenderer
from app.services.renderers.html_report_renderer import HTMLReportRenderer
from app.services.renderers.pdf_report_renderer import PDFReportRenderer
from app.services.renderers.markdown_report_renderer import MarkdownReportRenderer
from app.services.renderers.csv_evidence_renderer import CSVEvidenceRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO


class TestRendererInterface:
    """Test that all format renderers adhere to the universal BaseReportRenderer interface."""

    def _sample_doc(self):
        ov = TrustOverviewDTO(risk_score=25.0, risk_band="LOW_RISK")
        return ReportDocumentDTO(report_id="rep_1", analysis_id="an_1", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)

    def test_json_renderer_interface(self):
        r = JSONReportRenderer()
        assert isinstance(r, BaseReportRenderer)
        assert r.get_file_extension() == "json"
        assert "json" in r.get_content_type()
        assert r.get_renderer_version() == "1.0.0"

    def test_html_renderer_interface(self):
        r = HTMLReportRenderer()
        assert isinstance(r, BaseReportRenderer)
        assert r.get_file_extension() == "html"
        assert "html" in r.get_content_type()
        assert r.get_renderer_version() == "1.0.0"

    def test_pdf_renderer_interface(self):
        r = PDFReportRenderer()
        assert isinstance(r, BaseReportRenderer)
        assert r.get_file_extension() == "pdf"
        assert "pdf" in r.get_content_type()
        assert r.get_renderer_version() == "1.0.0"

    def test_markdown_renderer_interface(self):
        r = MarkdownReportRenderer()
        assert isinstance(r, BaseReportRenderer)
        assert r.get_file_extension() == "md"
        assert "markdown" in r.get_content_type()

    def test_csv_renderer_interface(self):
        r = CSVEvidenceRenderer()
        assert isinstance(r, BaseReportRenderer)
        assert r.get_file_extension() == "csv"
        assert "csv" in r.get_content_type()

    def test_calculate_size_and_hash(self):
        r = JSONReportRenderer()
        doc = self._sample_doc()
        data = r.render(doc)
        assert r.calculate_size(data) == len(data)
        assert len(r.calculate_hash(data)) == 64
