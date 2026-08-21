"""Unit Tests — Rendering Idempotency (Phase 4.0 Part 3 — Section 90)."""

import pytest
from app.services.report_rendering_engine import ReportRenderingEngine
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO


class TestRenderingIdempotency:
    """Section 90: Same report, version, format, and renderer produce consistent artifact hashes."""

    def test_idempotent_json_rendering(self):
        engine = ReportRenderingEngine()
        ov = TrustOverviewDTO(risk_score=40.0, risk_band="MODERATE_RISK")
        doc = ReportDocumentDTO(report_id="rep_idemp", analysis_id="an_idemp", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)

        art1, b1 = engine.render_artifact(doc, format_name="JSON")
        art2, b2 = engine.render_artifact(doc, format_name="JSON")

        assert art1.sha256 == art2.sha256
        assert b1 == b2
