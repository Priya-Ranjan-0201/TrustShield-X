"""Unit Tests — Claim Validator Numerical Consistency (Phase 4.0 Part 2)."""

import pytest
from app.services.claim_validator import ClaimValidator
from app.schemas.trust_narrative_models import (
    NarrativeDocumentDTO, ExecutiveSummaryNarrativeDTO, RiskNarrativeDTO,
)


class TestClaimValidatorNumericalConsistency:
    """Mandatory Test Case 14: Numerical consistency validation."""

    def setup_method(self):
        self.validator = ClaimValidator()

    def test_score_consistency(self):
        doc = NarrativeDocumentDTO(
            narrative_id="n1", report_id="r1", analysis_id="a1",
            executive_summary=ExecutiveSummaryNarrativeDTO(headline="H", overall_assessment="A"),
            risk_narrative=RiskNarrativeDTO(risk_statement="Risk Score: 85.0 / 100. Risk Band: HIGH_RISK. Confidence: HIGH. Evidence Sufficiency: SUFFICIENT."),
        )
        failures = self.validator.validate_document(doc, 85.0, "HIGH_RISK", "HIGH", "SUFFICIENT")
        score_failures = [f for f in failures if "Risk score" in f]
        assert len(score_failures) == 0

    def test_score_mismatch(self):
        doc = NarrativeDocumentDTO(
            narrative_id="n1", report_id="r1", analysis_id="a1",
            executive_summary=ExecutiveSummaryNarrativeDTO(headline="H", overall_assessment="A"),
            risk_narrative=RiskNarrativeDTO(risk_statement="Risk Score: 50.0 / 100. Risk Band: MODERATE_RISK."),
        )
        failures = self.validator.validate_document(doc, 85.0, "HIGH_RISK", "HIGH", "SUFFICIENT")
        assert any("Risk score" in f or "Risk band" in f for f in failures)

    def test_band_mismatch(self):
        doc = NarrativeDocumentDTO(
            narrative_id="n1", report_id="r1", analysis_id="a1",
            executive_summary=ExecutiveSummaryNarrativeDTO(headline="H", overall_assessment="A"),
            risk_narrative=RiskNarrativeDTO(risk_statement="Risk Score: 85.0. Risk Band: LOW_RISK."),
        )
        failures = self.validator.validate_document(doc, 85.0, "HIGH_RISK", "HIGH", "SUFFICIENT")
        assert any("Risk band" in f for f in failures)
