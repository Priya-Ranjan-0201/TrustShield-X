"""Unit Tests — JSON Schema Validation (Phase 4.0 Part 3 — Section 9)."""

import os
import json
import pytest
from app.services.renderers.json_report_renderer import JSONReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestJSONSchemaValidation:
    """Test that generated JSON conforms to digital_trust_report.schema.json."""

    def test_schema_file_exists_and_valid(self):
        schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "schemas", "digital_trust_report.schema.json")
        assert os.path.exists(schema_path)
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        assert schema["title"] == "DigitalTrustReportSchema"
        assert "required" in schema
        assert "trust_overview" in schema["required"]

    def test_rendered_json_contains_all_required_fields(self):
        r = JSONReportRenderer()
        ov = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        finding = ReportFindingDTO(finding_id="f_01", category="DATA", title="T", description="D")
        doc = ReportDocumentDTO(
            report_id="rep_schema_test",
            analysis_id="an_schema_test",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[finding],
        )
        out_bytes = r.render(doc)
        parsed = json.loads(out_bytes.decode("utf-8"))

        required_keys = ["report_id", "analysis_id", "report_version", "schema_version", "generated_at", "trust_overview", "risk_assessment"]
        for k in required_keys:
            assert k in parsed, f"Missing required schema key: {k}"
