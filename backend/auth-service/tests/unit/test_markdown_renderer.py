"""Unit Tests — Markdown Report Renderer (Phase 4.0 Part 3 — Section 84, Test 4)."""

import pytest
from app.services.renderers.markdown_report_renderer import MarkdownReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestMarkdownReportRenderer:
    """Mandatory Test Case 4: Generate Markdown and verify all major sections."""

    def test_markdown_major_sections(self):
        r = MarkdownReportRenderer()
        ov = TrustOverviewDTO(risk_score=70.0, risk_band="HIGH_RISK", confidence="HIGH", evidence_sufficiency="SUFFICIENT")
        f = ReportFindingDTO(finding_id="F_MD_01", category="DATAFLOW", title="Exfiltration to Remote Host", description="Personal data transferred over HTTP")
        ev = ReportEvidenceCardDTO(card_id="EV_MD_01", title="Cleartext Packet", category="NETWORK", observation="Unencrypted payload observed")
        doc = ReportDocumentDTO(
            report_id="rep_md_test",
            analysis_id="an_md_test",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            evidence_cards=[ev],
            recommendations=["Enforce HTTPS/TLS", "Revoke location access"],
            limitations=["Dynamic code loading not evaluated"],
        )

        out_bytes = r.render(doc)
        assert r.validate_output(out_bytes) is True
        text = out_bytes.decode("utf-8")

        assert "# Digital Trust Report" in text
        assert "## Executive Summary" in text
        assert "## Risk Assessment" in text
        assert "## Findings" in text
        assert "## Evidence" in text
        assert "## Recommendations" in text
        assert "## Limitations" in text
        assert "## Provenance" in text
        assert "## Technical Appendix" in text

        # Verify values
        assert "70.0" in text
        assert "HIGH_RISK" in text
        assert "F_MD_01" in text
        assert "Exfiltration to Remote Host" in text
        assert "Enforce HTTPS/TLS" in text
        assert "Dynamic code loading not evaluated" in text
