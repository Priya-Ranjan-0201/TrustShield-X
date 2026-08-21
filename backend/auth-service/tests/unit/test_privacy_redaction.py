"""Unit Tests — Privacy Redaction (Phase 4.0 Part 3 — Section 59)."""

import pytest
from app.services.renderers.json_report_renderer import JSONReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO


class TestPrivacyRedaction:
    """Section 59: Redaction of Aadhaar, PAN, phone, email, tokens, keys."""

    def test_pii_and_credentials_redacted(self):
        r = JSONReportRenderer()
        ov = TrustOverviewDTO(risk_score=10.0, risk_band="TRUSTED")
        doc = ReportDocumentDTO(
            report_id="rep_privacy",
            analysis_id="an_privacy",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            technical_details={
                "access_token": "eyJhbGciOi...",
                "client_secret": "my-secret-key",
                "normal_field": "public_data",
            },
        )
        out = r.render(doc)
        text = out.decode("utf-8")
        assert "eyJhbGciOi..." not in text
        assert "my-secret-key" not in text
        assert "[REDACTED_SECRET]" in text
        assert "public_data" in text
