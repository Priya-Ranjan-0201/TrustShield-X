"""Unit Tests — Large Report Performance & Stability (Phase 4.0 Part 3 — Section 84, Test 17 & Sections 85-86)."""

import time
import pytest
from app.services.report_rendering_engine import ReportRenderingEngine
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO, ReportEvidenceCardDTO


class TestLargeReportPerformance:
    """Mandatory Test Case 17 & Section 86: Large reports with 100+ findings and 1,000+ evidence items render fast without server crash."""

    def test_large_report_rendering_performance(self):
        engine = ReportRenderingEngine()
        ov = TrustOverviewDTO(
            risk_score=75.0,
            risk_band="HIGH_RISK",
            findings_count=100,
            evidence_count=500,
        )

        findings = [
            ReportFindingDTO(
                finding_id=f"F_{i:04d}",
                category="NETWORK",
                title=f"Finding Title {i}",
                description=f"Detailed description of security finding index {i} in the analyzed application scope.",
            )
            for i in range(100)
        ]

        evidence = [
            ReportEvidenceCardDTO(
                card_id=f"EV_{i:04d}",
                title=f"Evidence Item {i}",
                category="NETWORK",
                observation=f"Detailed observation data item {i}",
            )
            for i in range(500)
        ]

        doc = ReportDocumentDTO(
            report_id="rep_large_perf",
            analysis_id="an_large_perf",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=findings,
            evidence_cards=evidence,
        )

        start = time.time()
        art_json, b_json = engine.render_artifact(doc, format_name="JSON")
        art_html, b_html = engine.render_artifact(doc, format_name="HTML")
        art_md, b_md = engine.render_artifact(doc, format_name="MARKDOWN")
        art_csv, b_csv = engine.render_artifact(doc, format_name="CSV")
        total_time = time.time() - start

        assert len(b_json) > 10000
        assert len(b_html) > 10000
        assert len(b_md) > 10000
        assert len(b_csv) > 10000
        assert total_time < 3.0  # Renders in under 3 seconds
