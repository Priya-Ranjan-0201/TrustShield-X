"""Unit Tests — Investigation Concurrency & Thread Safety (Phase 4.0 Part 4 — Section 83)."""

import pytest
import concurrent.futures
from app.services.investigation_orchestrator import InvestigationOrchestrator
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestInvestigationConcurrency:
    def test_concurrent_evidence_graph_building(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=60.0, risk_band="MODERATE_RISK")
        f = ReportFindingDTO(finding_id="F_CONC_01", category="NETWORK", title="Net Leak", description="HTTP")
        doc = ReportDocumentDTO(report_id="rep_conc", analysis_id="an_conc", generated_at="2026-08-14T00:00:00Z", trust_overview=ov, major_findings=[f])

        def _run_graph():
            return orch.build_evidence_graph(doc)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(_run_graph) for _ in range(10)]
            results = [f.result() for f in futures]

        assert len(results) == 10
        for r in results:
            assert r.analysis_id == "an_conc"
            assert r.total_nodes >= 2
