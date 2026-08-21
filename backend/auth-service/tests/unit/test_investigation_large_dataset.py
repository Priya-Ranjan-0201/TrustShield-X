"""Unit Tests — Large Dataset Truncation & Progressive Loading (Phase 4.0 Part 4 — Sections 55-57, 88)."""

import pytest
from app.services.investigation_orchestrator import InvestigationOrchestrator
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
)


class TestInvestigationLargeDataset:
    def test_graph_truncates_at_limit(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=70.0, risk_band="HIGH_RISK")
        findings = [
            ReportFindingDTO(finding_id=f"F_LARGE_{i}", category="STORAGE", title=f"Finding {i}", description="Desc")
            for i in range(500)
        ]
        evidence = [
            ReportEvidenceCardDTO(card_id=f"EV_LARGE_{i}", category="STORAGE", title=f"Ev {i}", observation="Obs")
            for i in range(500)
        ]
        doc = ReportDocumentDTO(
            report_id="rep_large",
            analysis_id="an_large",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=findings,
            evidence_cards=evidence,
        )

        # Build with limit=50
        graph = orch.build_evidence_graph(doc, limit=50)
        assert graph.truncated is True
        assert len(graph.nodes) <= 105  # Root + Risk + 50 findings + 50 evidence
