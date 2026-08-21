"""Unit Tests — Investigation Pagination (Phase 4.0 Part 4 — Section 55, 83)."""

import pytest
from app.services.investigation_orchestrator import InvestigationOrchestrator
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
)


class TestInvestigationPagination:
    def test_search_results_pagination_limit(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        findings = [
            ReportFindingDTO(finding_id=f"F_PAGE_{i}", category="NETWORK", title=f"Leak {i}", description=f"HTTP endpoint {i}")
            for i in range(100)
        ]
        doc = ReportDocumentDTO(
            report_id="rep_page",
            analysis_id="an_page",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=findings,
        )

        res = orch.search_investigation(query="Leak", doc=doc, limit=20)
        assert len(res.results) == 20
        assert res.total_results == 100
