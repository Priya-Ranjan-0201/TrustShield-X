"""Unit Tests — Investigation Timeline (Phase 4.0 Part 4 — Sections 19-20, 83)."""

import pytest
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
)
from app.services.investigation_orchestrator import InvestigationOrchestrator


class TestTimelineAPI:
    def test_timeline_event_generation(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=68.0, risk_band="MODERATE_RISK", confidence="HIGH")
        f = ReportFindingDTO(finding_id="F_TIME_01", category="STORAGE", title="Insecure Key", description="Stored plain", severity_reference="MEDIUM")
        ev = ReportEvidenceCardDTO(card_id="EV_TIME_01", category="STORAGE", title="Key file", observation="read key", finding_reference="F_TIME_01")
        doc = ReportDocumentDTO(
            report_id="rep_time_01",
            analysis_id="an_time_01",
            generated_at="2026-08-14T10:00:00Z",
            trust_overview=ov,
            major_findings=[f],
            evidence_cards=[ev],
        )

        timeline = orch.build_timeline(doc)
        assert timeline.analysis_id == "an_time_01"
        assert timeline.total_events >= 4  # STARTED, EVIDENCE_OBSERVED, FINDING_CREATED, RISK_ASSESSMENT, REPORT_GENERATED
        types = [e.event_type for e in timeline.events]
        assert "ANALYSIS_STARTED" in types
        assert "EVIDENCE_OBSERVED" in types
        assert "FINDING_CREATED" in types
        assert "RISK_ASSESSMENT" in types
        assert "REPORT_GENERATED" in types
