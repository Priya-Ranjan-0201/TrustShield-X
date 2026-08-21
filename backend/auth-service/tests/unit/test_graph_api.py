"""Unit Tests — Graph API & Construction (Phase 4.0 Part 4 — Sections 13-16, 83)."""

import pytest
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
)
from app.services.investigation_orchestrator import InvestigationOrchestrator


class TestGraphAPI:
    def test_build_evidence_graph_nodes_and_edges(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=75.0, risk_band="HIGH_RISK")
        f = ReportFindingDTO(finding_id="F_GRAPH_01", category="NETWORK", title="HTTP Leak", description="Cleartext", severity_reference="HIGH")
        ev = ReportEvidenceCardDTO(card_id="EV_GRAPH_01", category="NETWORK", title="Packet Capture", observation="cleartext url", finding_reference="F_GRAPH_01")
        doc = ReportDocumentDTO(
            report_id="rep_graph_01",
            analysis_id="an_graph_01",
            generated_at="2026-08-14T00:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            evidence_cards=[ev],
        )

        graph = orch.build_evidence_graph(doc)
        assert graph.analysis_id == "an_graph_01"
        assert graph.total_nodes >= 3  # Root analysis, Risk Factor, Finding, Evidence
        assert graph.total_edges >= 2
        
        # Check node types
        types = [n.type for n in graph.nodes]
        assert "ANALYSIS" in types
        assert "RISK_FACTOR" in types
        assert "FINDING" in types
        assert "EVIDENCE" in types
