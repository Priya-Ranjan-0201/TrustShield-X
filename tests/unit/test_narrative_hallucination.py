"""Unit Tests — Claim Validator Hallucination Detection (Phase 4.0 Part 2)."""

import pytest
from app.services.claim_validator import ClaimValidator
from app.schemas.trust_narrative_models import (
    NarrativeDocumentDTO, ExecutiveSummaryNarrativeDTO, RiskNarrativeDTO,
    NarrativeStatementDTO,
)


class TestClaimValidatorHallucination:
    """Mandatory Test Case 13: Hallucination detection catches unsupported claims."""

    def setup_method(self):
        self.validator = ClaimValidator()

    def _make_doc(self, headline="Test", overall="Test", risk_stmt="Risk Score: 50.0. Risk Band: MODERATE_RISK.", extra_stmts=None):
        exec_sum = ExecutiveSummaryNarrativeDTO(headline=headline, overall_assessment=overall)
        risk_narr = RiskNarrativeDTO(risk_statement=risk_stmt)
        stmts = extra_stmts or []
        return NarrativeDocumentDTO(
            narrative_id="n1", report_id="r1", analysis_id="a1",
            executive_summary=exec_sum, risk_narrative=risk_narr, statements=stmts,
        )

    def test_hallucination_confirmed_malware(self):
        doc = self._make_doc(headline="confirmed malware detected")
        failures = self.validator.validate_document(doc, 50.0, "MODERATE_RISK", "MEDIUM", "LIMITED")
        assert any("HALLUCINATION" in f for f in failures)

    def test_hallucination_attacker(self):
        doc = self._make_doc(overall="The attacker deployed a trojan.")
        failures = self.validator.validate_document(doc, 50.0, "MODERATE_RISK", "MEDIUM", "LIMITED")
        assert any("HALLUCINATION" in f for f in failures)

    def test_hallucination_steals(self):
        stmt = NarrativeStatementDTO(statement_id="s1", claim="this app steals user data")
        doc = self._make_doc(extra_stmts=[stmt])
        failures = self.validator.validate_document(doc, 50.0, "MODERATE_RISK", "MEDIUM", "LIMITED")
        assert any("HALLUCINATION" in f for f in failures)

    def test_no_hallucination(self):
        doc = self._make_doc(headline="Digital Trust Assessment", overall="Low indicators observed",
                             risk_stmt="Risk Score: 20.0. Risk Band: LOW_RISK.")
        failures = self.validator.validate_document(doc, 20.0, "LOW_RISK", "HIGH", "SUFFICIENT")
        hallucination_failures = [f for f in failures if "HALLUCINATION" in f]
        assert len(hallucination_failures) == 0
