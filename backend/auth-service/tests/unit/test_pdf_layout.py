"""Unit Tests — PDF Layout & Page Structure (Phase 4.0 Part 3 — Section 30)."""

import pytest
from app.services.renderers.pdf_report_renderer import PDFReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportProvenanceDTO


class TestPDFLayout:
    """Section 30: Test PDF sections for Cover, Executive Summary, Risk, Findings, Provenance, Appendix."""

    def test_pdf_sections_and_provenance(self):
        r = PDFReportRenderer()
        ov = TrustOverviewDTO(risk_score=15.0, risk_band="LOW_RISK")
        prov = ReportProvenanceDTO(statement_id="stmt_01", source_module="NetworkEngine", finding_id="f_01", evidence_id="ev_01", timestamp="2026-08-14T00:00:00Z")
        doc = ReportDocumentDTO(
            report_id="rep_layout",
            analysis_id="an_layout",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            provenance=[prov],
        )

        out_bytes = r.render(doc)
        text = out_bytes.decode("latin1", errors="ignore")

        assert "EXECUTIVE SUMMARY" in text
        assert "TRUST OVERVIEW & RISK ASSESSMENT" in text
        assert "TECHNICAL APPENDIX & PROVENANCE" in text
        assert "stmt_01" in text
        assert "NetworkEngine" in text
