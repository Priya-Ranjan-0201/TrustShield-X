"""Unit Tests — Cross-Modal Correlations (Phase 4.0 Part 4 — Sections 17-18, 83)."""

import pytest
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
)
from app.services.investigation_orchestrator import InvestigationOrchestrator


class TestCrossModalCorrelations:
    def test_cross_modal_correlation_synthesis(self):
        orch = InvestigationOrchestrator()
        ov = TrustOverviewDTO(risk_score=70.0, risk_band="HIGH_RISK")
        
        # Report A: APK analysis
        f1 = ReportFindingDTO(finding_id="F_APK_01", category="NETWORK", title="C2 Domain Found", description="Found evil.com")
        doc_apk = ReportDocumentDTO(report_id="rep_apk", analysis_id="an_apk", generated_at="2026-08-14T00:00:00Z", trust_overview=ov, major_findings=[f1])

        # Report B: Website analysis
        f2 = ReportFindingDTO(finding_id="F_WEB_01", category="NETWORK", title="Phishing Host", description="evil.com phishing bank")
        doc_web = ReportDocumentDTO(report_id="rep_web", analysis_id="an_web", generated_at="2026-08-14T00:00:00Z", trust_overview=ov, major_findings=[f2])

        corrs = orch.build_cross_modal_correlations(
            case_id="case_multimodal_01",
            analyses=[],
            reports=[doc_apk, doc_web],
        )

        assert corrs.case_id == "case_multimodal_01"
        assert corrs.total_correlations >= 1
        c = corrs.correlations[0]
        assert c.source_analysis_id == "an_apk"
        assert c.target_analysis_id == "an_web"
        assert c.relationship == "CORRELATED_WITH"
