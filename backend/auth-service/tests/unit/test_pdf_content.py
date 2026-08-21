"""Unit Tests — PDF Content Verification (Phase 4.0 Part 3 — Section 84, Test 3)."""

import pytest
from app.services.renderers.pdf_report_renderer import PDFReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestPDFContentVerification:
    """Mandatory Test Case 3 & Section 72: Generate PDF, extract text, verify required report content."""

    def test_pdf_contains_authoritative_text(self):
        r = PDFReportRenderer()
        ov = TrustOverviewDTO(risk_score=92.5, risk_band="CRITICAL_RISK", confidence="VERY_HIGH", evidence_sufficiency="SUFFICIENT")
        f = ReportFindingDTO(finding_id="F_CRIT_01", category="RANSOMWARE", title="File Encryption Observed", description="Cryptographic operations on external storage")
        ev = ReportEvidenceCardDTO(card_id="EV_01", title="Key Generation", category="CRYPTO", observation="AES key generated")
        doc = ReportDocumentDTO(
            report_id="rep_crit_pdf",
            analysis_id="an_crit_pdf",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            evidence_cards=[ev],
            recommendations=["Immediate uninstall", "Block C2 IP at gateway"],
            limitations=["Static analysis only"],
        )

        out_bytes = r.render(doc)
        text = out_bytes.decode("latin1", errors="ignore")

        # Verify exact required content exists inside PDF streams
        assert "rep_crit_pdf" in text
        assert "92.5" in text
        assert "CRITICAL_RISK" in text
        assert "VERY_HIGH" in text
        assert "SUFFICIENT" in text
        assert "F_CRIT_01" in text
        assert "File Encryption Observed" in text
        assert "Immediate uninstall" in text
        assert "Static analysis only" in text
