"""Unit Tests — Trust Narrative Orchestrator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_orchestrator import TrustNarrativeOrchestrator


class TestTrustNarrativeOrchestrator:
    """Mandatory Test Case 17: Orchestrator generates and validates narratives."""

    def setup_method(self):
        self.orch = TrustNarrativeOrchestrator()

    def test_generate_valid_narrative(self):
        risk_dto = SimpleNamespace(risk_score=25.0, risk_band="LOW_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="NETWORK_THREAT")
        doc = self.orch.generate_narrative("r1", "a1", risk_assessment_dto=risk_dto)
        assert doc.narrative_id == "narr_r1"
        assert doc.validation is not None

    def test_orchestrator_missing_risk(self):
        with pytest.raises(ValueError, match="Missing RiskAssessment"):
            self.orch.generate_narrative("r1", "a1", risk_assessment_dto=None)

    def test_orchestrator_validation_attached(self):
        risk_dto = SimpleNamespace(risk_score=50.0, risk_band="MODERATE_RISK", confidence_level="MEDIUM", evidence_sufficiency="LIMITED", primary_risk_category="DATA_LEAK")
        doc = self.orch.generate_narrative("r2", "a2", risk_assessment_dto=risk_dto)
        assert doc.validation is not None
        assert doc.validation.checks_performed > 0

    def test_orchestrator_metrics(self):
        risk_dto = SimpleNamespace(risk_score=25.0, risk_band="LOW_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="NETWORK_THREAT")
        self.orch.generate_narrative("r1", "a1", risk_assessment_dto=risk_dto)
        m = self.orch.get_metrics()
        assert m.narratives_generated_total >= 1

    def test_orchestrator_llm_disabled(self):
        assert self.orch.llm_adapter.enabled is False
