"""Unit Tests — Investigation Search & Authorization (Phase 4.0 Part 4 — Sections 52-54, 83)."""

import pytest
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
)
from app.services.investigation_orchestrator import InvestigationOrchestrator


class TestSearchAuthorization:
    def test_search_investigation_returns_matching_objects(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        f = ReportFindingDTO(finding_id="F_SEARCH_01", category="NETWORK", title="Malicious C2 Host", description="Connects to api.c2-host.com")
        ev = ReportEvidenceCardDTO(card_id="EV_SEARCH_01", category="NETWORK", title="Domain Reference", observation="api.c2-host.com")
        doc = ReportDocumentDTO(
            report_id="rep_search",
            analysis_id="an_search",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            evidence_cards=[ev],
        )

        res = orch.search_investigation("c2-host", doc)
        assert res.total_results >= 2
        types = [r.object_type for r in res.results]
        assert "FINDING" in types
        assert "EVIDENCE" in types

    def test_search_investigation_empty_query(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        doc = ReportDocumentDTO(report_id="rep_01", analysis_id="an_01", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        res = orch.search_investigation("", doc)
        assert res.total_results == 0
