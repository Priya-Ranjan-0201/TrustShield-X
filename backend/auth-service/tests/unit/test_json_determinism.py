"""Unit Tests — JSON Determinism (Phase 4.0 Part 3 — Section 8)."""

import pytest
from app.services.renderers.json_report_renderer import JSONReportRenderer
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestJSONDeterminism:
    """Section 8: Given identical inputs, JSON output must be byte-for-byte identical."""

    def test_json_determinism_multiple_runs(self):
        r = JSONReportRenderer()
        ov = TrustOverviewDTO(risk_score=60.0, risk_band="MODERATE_RISK")
        f1 = ReportFindingDTO(finding_id="f_02", category="API", title="T2", description="D2")
        f2 = ReportFindingDTO(finding_id="f_01", category="NET", title="T1", description="D1")
        ev1 = ReportEvidenceCardDTO(card_id="c_02", title="E2", category="NET", observation="O2")
        ev2 = ReportEvidenceCardDTO(card_id="c_01", title="E1", category="API", observation="O1")

        doc = ReportDocumentDTO(
            report_id="rep_det",
            analysis_id="an_det",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f1, f2],  # Out of order
            evidence_cards=[ev1, ev2],  # Out of order
            recommendations=["Rec B", "Rec A"],
        )

        out1 = r.render(doc)
        out2 = r.render(doc)
        out3 = r.render(doc)

        assert out1 == out2 == out3
        assert r.calculate_hash(out1) == r.calculate_hash(out2)
