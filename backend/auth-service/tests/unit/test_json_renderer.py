"""Unit Tests — JSON Report Renderer (Phase 4.0 Part 3 — Section 84, Test 1)."""

import json
import pytest
from app.services.renderers.json_report_renderer import JSONReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestJSONReportRenderer:
    """Mandatory Test Case 1: Generate JSON and verify schema and authoritative risk values."""

    def test_json_render_exact_values(self):
        r = JSONReportRenderer()
        ov = TrustOverviewDTO(risk_score=85.5, risk_band="HIGH_RISK", confidence="HIGH", evidence_sufficiency="SUFFICIENT")
        finding = ReportFindingDTO(finding_id="f_01", category="NETWORK", title="Malicious C2", description="C2 connection detected")
        doc = ReportDocumentDTO(
            report_id="rep_test_json",
            analysis_id="an_test_json",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[finding],
        )

        out_bytes = r.render(doc)
        assert r.validate_output(out_bytes) is True

        parsed = json.loads(out_bytes.decode("utf-8"))
        assert parsed["report_id"] == "rep_test_json"
        assert parsed["trust_overview"]["risk_score"] == 85.5
        assert parsed["trust_overview"]["risk_band"] == "HIGH_RISK"
        assert parsed["trust_overview"]["confidence"] == "HIGH"
        assert parsed["trust_overview"]["evidence_sufficiency"] == "SUFFICIENT"
        assert len(parsed["major_findings"]) == 1
        assert parsed["major_findings"][0]["finding_id"] == "f_01"

    def test_json_secrets_redaction(self):
        r = JSONReportRenderer()
        ov = TrustOverviewDTO(risk_score=10.0, risk_band="TRUSTED")
        doc = ReportDocumentDTO(
            report_id="rep_sec",
            analysis_id="an_sec",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            technical_details={"api_key": "secret123", "db_password": "pass", "safe_param": "ok"},
        )
        out_bytes = r.render(doc)
        parsed = json.loads(out_bytes.decode("utf-8"))
        assert parsed["technical_details"]["api_key"] == "[REDACTED_SECRET]"
        assert parsed["technical_details"]["db_password"] == "[REDACTED_SECRET]"
        assert parsed["technical_details"]["safe_param"] == "ok"
