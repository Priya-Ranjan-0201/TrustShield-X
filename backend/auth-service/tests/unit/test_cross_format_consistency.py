"""Unit Tests — Cross-Format Parity & Consistency (Phase 4.0 Part 3 — Section 84, Test 9)."""

import pytest
from app.services.report_rendering_engine import ReportRenderingEngine
from app.services.cross_format_validator import CrossFormatValidator
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestCrossFormatConsistency:
    """Mandatory Test Case 9: Render JSON, HTML, PDF, and Markdown.

    Expected: Same authoritative risk, band, confidence, evidence sufficiency, findings, recommendations.
    """

    def test_all_formats_preserve_authoritative_values(self):
        engine = ReportRenderingEngine()
        validator = CrossFormatValidator()

        ov = TrustOverviewDTO(
            risk_score=82.5,
            risk_band="HIGH_RISK",
            confidence="VERY_HIGH",
            evidence_sufficiency="SUFFICIENT",
            findings_count=1,
            evidence_count=1,
        )
        f = ReportFindingDTO(finding_id="F_CONSIST_01", category="NETWORK", title="C2 Observed", description="Direct socket communication")
        doc = ReportDocumentDTO(
            report_id="rep_parity_test",
            analysis_id="an_parity_test",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            recommendations=["Revoke internet permission"],
        )

        rendered_map = {}
        for fmt in ["JSON", "HTML", "PDF", "MARKDOWN", "CSV"]:
            _, b = engine.render_artifact(report_doc=doc, format_name=fmt)
            rendered_map[fmt] = b

        res = validator.validate_consistency(doc, rendered_map)
        assert res.consistent is True
        assert len(res.discrepancies) == 0
