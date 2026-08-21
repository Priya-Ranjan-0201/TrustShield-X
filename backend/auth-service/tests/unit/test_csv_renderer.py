"""Unit Tests — CSV Evidence Renderer (Phase 4.0 Part 3 — Section 84, Test 5)."""

import csv
import io
import pytest
from app.services.renderers.csv_evidence_renderer import CSVEvidenceRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestCSVEvidenceRenderer:
    """Mandatory Test Case 5: Generate CSV and verify evidence references and columns."""

    def test_csv_evidence_columns_and_rows(self):
        r = CSVEvidenceRenderer()
        ov = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        f = ReportFindingDTO(finding_id="F_CSV_01", category="STORAGE", title="Insecure Database", description="Plaintext DB")
        ev = ReportEvidenceCardDTO(card_id="EV_CSV_01", title="SQLite File", category="STORAGE", observation="world readable", source="STORAGE", finding_reference="F_CSV_01")
        doc = ReportDocumentDTO(
            report_id="rep_csv_test",
            analysis_id="an_csv_test",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            evidence_cards=[ev],
        )

        out_bytes = r.render(doc)
        assert r.validate_output(out_bytes) is True

        reader = csv.DictReader(io.StringIO(out_bytes.decode("utf-8")))
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["report_id"] == "rep_csv_test"
        assert rows[0]["analysis_id"] == "an_csv_test"
        assert rows[0]["finding_id"] == "F_CSV_01"
        assert rows[0]["evidence_id"] == "EV_CSV_01"
        assert rows[0]["source_module"] == "STORAGE"
        assert rows[0]["resolution_status"] == "RESOLVED"
