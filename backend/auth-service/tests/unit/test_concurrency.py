"""Unit Tests — Concurrency & Multi-User Isolation (Phase 4.0 Part 3 — Section 84, Test 18 & Section 87)."""

import pytest
import concurrent.futures
from app.services.report_rendering_engine import ReportRenderingEngine
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO


class TestConcurrency:
    """Mandatory Test Case 18 & Section 87: Generate report concurrently for multiple users without cross-analysis contamination."""

    def test_concurrent_report_rendering(self):
        engine = ReportRenderingEngine()

        def _render_report(idx: int):
            ov = TrustOverviewDTO(risk_score=float(idx * 10), risk_band="LOW_RISK" if idx < 5 else "HIGH_RISK")
            doc = ReportDocumentDTO(
                report_id=f"rep_concurrent_{idx}",
                analysis_id=f"an_concurrent_{idx}",
                generated_at="2026-08-14T00:00:00Z",
                trust_overview=ov,
            )
            art, b = engine.render_artifact(doc, format_name="JSON")
            return idx, art.report_id, b

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(_render_report, i) for i in range(1, 11)]
            results = [f.result() for f in futures]

        # Verify no contamination
        for idx, rep_id, b in results:
            assert rep_id == f"rep_concurrent_{idx}"
            assert f"rep_concurrent_{idx}".encode("utf-8") in b
