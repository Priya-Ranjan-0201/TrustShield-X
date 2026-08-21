"""Unit Tests — HTML XSS Injection Prevention (Phase 4.0 Part 3 — Section 84, Test 6)."""

import pytest
from app.services.renderers.html_report_renderer import HTMLReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestHTMLXSSPrevention:
    """Mandatory Test Case 6: Insert malicious HTML into evidence description. Expected: Escaped safely."""

    def test_malicious_html_in_evidence_escaped(self):
        r = HTMLReportRenderer()
        ov = TrustOverviewDTO(risk_score=75.0, risk_band="HIGH_RISK")
        malicious_evidence = ReportEvidenceCardDTO(
            card_id="ev_xss_01",
            title="<img src=x onerror=alert('xss')>",
            category="NETWORK",
            observation="<svg onload=alert(document.cookie)>Malicious observation</svg>",
        )
        malicious_finding = ReportFindingDTO(
            finding_id="f_xss",
            category="NET",
            title="<script>alert(1)</script>",
            description="<a href='javascript:alert(1)'>Click me</a>",
        )
        doc = ReportDocumentDTO(
            report_id="rep_xss",
            analysis_id="an_xss",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[malicious_finding],
            evidence_cards=[malicious_evidence],
            recommendations=["<b onmouseover=alert(1)>Malicious Rec</b>"],
        )

        out_bytes = r.render(doc)
        text = out_bytes.decode("utf-8")

        # Unescaped payload strings MUST NOT exist in HTML
        assert "<img src=x onerror=alert('xss')>" not in text
        assert "<svg onload=alert(document.cookie)>" not in text
        assert "<script>alert(1)</script>" not in text
        assert "<b onmouseover=alert(1)>" not in text

        # Escaped representations MUST exist
        assert "&lt;img src=x onerror=alert(&#x27;xss&#x27;)&gt;" in text or "&lt;img" in text
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in text
