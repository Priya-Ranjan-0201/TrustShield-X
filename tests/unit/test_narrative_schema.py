"""Unit Tests — Trust Narrative DTO Schema Validation (Phase 4.0 Part 2)."""

import pytest
from app.schemas.trust_narrative_models import (
    NarrativeStatementDTO, NarrativeDocumentDTO, ExecutiveSummaryNarrativeDTO,
    RiskNarrativeDTO, FindingNarrativeDTO, EvidenceNarrativeDTO,
    ContradictionNarrativeDTO, NarrativeLineageDTO, NarrativeVersionDTO,
    NarrativeValidationDTO, NarrativeMetricDTO,
)


class TestNarrativeSchemaValidation:
    """Mandatory Test Case 1: Schema Validation — All DTOs must pass validation."""

    def test_narrative_statement_dto(self):
        dto = NarrativeStatementDTO(statement_id="s1", claim="Test claim")
        assert dto.statement_id == "s1"
        assert dto.statement_type == "OBSERVATION"
        assert dto.claim_strength == "SUPPORTED"
        assert dto.confidence == "HIGH"
        assert dto.model_config.get("frozen") is True

    def test_executive_summary_dto(self):
        dto = ExecutiveSummaryNarrativeDTO(headline="H", overall_assessment="A")
        assert dto.headline == "H"
        assert isinstance(dto.top_findings, list)
        assert dto.model_config.get("frozen") is True

    def test_risk_narrative_dto(self):
        dto = RiskNarrativeDTO(risk_statement="Risk")
        assert dto.risk_statement == "Risk"
        assert isinstance(dto.category_explanations, list)

    def test_finding_narrative_dto(self):
        dto = FindingNarrativeDTO(finding_id="f1", title="T", what_was_found="W")
        assert dto.finding_id == "f1"
        assert dto.confidence == "HIGH"

    def test_evidence_narrative_dto(self):
        dto = EvidenceNarrativeDTO(evidence_id="e1", what_was_observed="O")
        assert dto.evidence_id == "e1"
        assert dto.evidence_strength == "STRONG"

    def test_contradiction_narrative_dto(self):
        dto = ContradictionNarrativeDTO(contradiction_id="c1", narrative="N", evidence_a="A", evidence_b="B")
        assert dto.resolution_status == "UNRESOLVED"

    def test_lineage_dto(self):
        dto = NarrativeLineageDTO(statement_id="s1", report_id="r1", section_id="sec1", source_type="FINDING", source_id="f1")
        assert dto.generated_by == "TrustNarrativeEngine"

    def test_version_dto(self):
        dto = NarrativeVersionDTO(narrative_id="n1")
        assert dto.schema_version == "4.0.0"
        assert dto.change_reason == "INITIAL_GENERATION"

    def test_validation_dto(self):
        dto = NarrativeValidationDTO(validation_id="v1", narrative_id="n1")
        assert dto.passed is True
        assert dto.checks_failed == 0

    def test_metric_dto(self):
        dto = NarrativeMetricDTO()
        assert dto.narratives_generated_total == 1
        assert dto.llm_requests_total == 0

    def test_narrative_document_dto(self):
        exec_sum = ExecutiveSummaryNarrativeDTO(headline="H", overall_assessment="A")
        risk_narr = RiskNarrativeDTO(risk_statement="R")
        doc = NarrativeDocumentDTO(
            narrative_id="n1", report_id="r1", analysis_id="a1",
            executive_summary=exec_sum, risk_narrative=risk_narr,
        )
        assert doc.narrative_id == "n1"
        assert doc.schema_version == "4.0.0"
        assert doc.mode == "DETERMINISTIC_MODE"
        assert doc.status == "COMPLETED"
        assert doc.model_config.get("frozen") is True
