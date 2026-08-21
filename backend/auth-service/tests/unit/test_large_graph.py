"""Large Graph Performance and Concurrency Tests (Phase 4.0 Part 5 — Sections 88-90)."""

import pytest
import concurrent.futures
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
)
from app.services.intelligence_graph_engine import IntelligenceGraphEngine


class TestLargeGraphAndConcurrency:
    def test_large_graph_processing_100_entities(self):
        engine = IntelligenceGraphEngine()
        ov = TrustOverviewDTO(risk_score=80.0, risk_band="HIGH_RISK")
        findings = [
            ReportFindingDTO(finding_id=f"F_PERF_{i}", category="STORAGE", title=f"Finding {i}", description="Desc", severity_reference="MEDIUM")
            for i in range(50)
        ]
        evidence = [
            ReportEvidenceCardDTO(card_id=f"EV_PERF_{i}", category="STORAGE", title=f"Ev {i}", observation="Obs")
            for i in range(50)
        ]
        doc = ReportDocumentDTO(
            report_id="rep_perf",
            analysis_id="an_perf",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=findings,
            evidence_cards=evidence,
        )

        graph, snap, run = engine.build_intelligence_graph([doc])
        assert graph.total_nodes >= 100
        assert run.status == "COMPLETED"

    def test_concurrent_intelligence_graph_building(self):
        engine = IntelligenceGraphEngine()
        ov = TrustOverviewDTO(risk_score=60.0, risk_band="MODERATE_RISK")
        f = ReportFindingDTO(finding_id="F_CONC", category="NETWORK", title="HTTP", description="desc", severity_reference="LOW")
        doc = ReportDocumentDTO(report_id="rep_c", analysis_id="an_c", generated_at="2026-08-14T00:00:00Z", trust_overview=ov, major_findings=[f])

        def _run_build():
            return engine.build_intelligence_graph([doc])

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(_run_build) for _ in range(8)]
            results = [f.result() for f in futures]

        assert len(results) == 8
        for g, snap, run in results:
            assert g.total_nodes >= 1
            assert run.status == "COMPLETED"
