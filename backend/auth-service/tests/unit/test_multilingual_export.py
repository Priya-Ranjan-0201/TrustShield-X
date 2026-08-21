"""Unit Tests — Multilingual Export (Phase 4.0 Part 3 — Section 84, Tests 19 & 20)."""

import pytest
from app.services.report_rendering_engine import ReportRenderingEngine
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestMultilingualExport:
    """Mandatory Tests 19 & 20: Generate Hindi and Punjabi reports.

    Expected: Same analytical values (risk score, band, finding IDs) and language metadata.
    """

    def test_hindi_report_preserves_analytical_values(self):
        engine = ReportRenderingEngine()
        ov = TrustOverviewDTO(risk_score=65.0, risk_band="MODERATE_RISK", confidence="HIGH", evidence_sufficiency="SUFFICIENT")
        f = ReportFindingDTO(finding_id="F_HI_01", category="NETWORK", title="शीर्षक", description="विवरण")
        doc_hi = ReportDocumentDTO(
            report_id="rep_hi",
            analysis_id="an_hi",
            language="hi",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
        )

        art, html_bytes = engine.render_artifact(doc_hi, format_name="HTML")
        text = html_bytes.decode("utf-8")
        assert 'lang="hi"' in text
        assert "65.0" in text
        assert "MODERATE_RISK" in text
        assert "F_HI_01" in text

    def test_punjabi_report_preserves_analytical_values(self):
        engine = ReportRenderingEngine()
        ov = TrustOverviewDTO(risk_score=80.0, risk_band="HIGH_RISK", confidence="HIGH", evidence_sufficiency="SUFFICIENT")
        f = ReportFindingDTO(finding_id="F_PA_01", category="STORAGE", title="ਸਿਰਲੇਖ", description="ਵੇਰਵਾ")
        doc_pa = ReportDocumentDTO(
            report_id="rep_pa",
            analysis_id="an_pa",
            language="pa",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
        )

        art, html_bytes = engine.render_artifact(doc_pa, format_name="HTML")
        text = html_bytes.decode("utf-8")
        assert 'lang="pa"' in text
        assert "80.0" in text
        assert "HIGH_RISK" in text
        assert "F_PA_01" in text
