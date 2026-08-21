"""Pydantic v2 DTO Schemas for Deterministic Executive Summary & Explainable Trust Narrative Engine (Phase 4.0 Part 2).

Strictly typed DTOs for narrative statements, documents, executive summaries, risk narratives,
finding narratives, evidence narratives, contradiction narratives, lineage, versions, validation, and metrics.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Section 2-4: Narrative Statement with claim types, claim strength, provenance
# ---------------------------------------------------------------------------

class NarrativeStatementDTO(BaseModel):
    """A single traceable narrative statement grounded in structured source data."""
    statement_id: str
    statement_type: str = "OBSERVATION"  # OBSERVATION, FINDING, CORRELATION, RISK_EXPLANATION, THREAT_INTELLIGENCE, DATAFLOW, BEHAVIOR, MITIGATION, PROTECTIVE_CONTROL, CONTRADICTION, UNCERTAINTY, RECOMMENDATION, LIMITATION, SYSTEM_STATUS
    source_type: str = "FINDING"  # FINDING, EVIDENCE, RISK_FACTOR, MODULE_RESULT, THREAT_MATCH, DATAFLOW_PATH, BEHAVIOR_CHAIN, RECOMMENDATION, LIMITATION
    source_id: str = ""
    claim: str
    claim_strength: str = "SUPPORTED"  # DIRECTLY_OBSERVED, STRONGLY_SUPPORTED, SUPPORTED, CORRELATED, INFERRED, PARTIALLY_SUPPORTED, UNRESOLVED, CONFLICTED, UNKNOWN
    confidence: str = "HIGH"
    provenance: str = ""
    limitations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 7: Executive Summary
# ---------------------------------------------------------------------------

class ExecutiveSummaryNarrativeDTO(BaseModel):
    headline: str
    overall_assessment: str
    primary_concern: str = ""
    top_findings: List[str] = Field(default_factory=list)
    risk_explanation: str = ""
    recommended_action: str = ""
    confidence_statement: str = ""
    limitations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 9: Risk Narrative
# ---------------------------------------------------------------------------

class RiskNarrativeDTO(BaseModel):
    risk_statement: str
    primary_risk_explanation: str = ""
    category_explanations: List[str] = Field(default_factory=list)
    top_contributing_factors: List[str] = Field(default_factory=list)
    mitigating_factors: List[str] = Field(default_factory=list)
    protective_factors: List[str] = Field(default_factory=list)
    uncertainty: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 14: Finding Narrative
# ---------------------------------------------------------------------------

class FindingNarrativeDTO(BaseModel):
    finding_id: str
    title: str
    what_was_found: str
    evidence: List[str] = Field(default_factory=list)
    supporting_modules: List[str] = Field(default_factory=list)
    confidence: str = "HIGH"
    why_it_matters: str = ""
    what_is_not_established: str = ""
    recommended_action: str = ""
    provenance: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 13: Evidence Narrative
# ---------------------------------------------------------------------------

class EvidenceNarrativeDTO(BaseModel):
    evidence_id: str
    what_was_observed: str
    why_it_matters: str = ""
    evidence_strength: str = "STRONG"
    source: str = ""
    limitations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 18: Contradiction Narrative
# ---------------------------------------------------------------------------

class ContradictionNarrativeDTO(BaseModel):
    contradiction_id: str
    narrative: str
    evidence_a: str
    evidence_b: str
    resolution_status: str = "UNRESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 45: Narrative Lineage
# ---------------------------------------------------------------------------

class NarrativeLineageDTO(BaseModel):
    statement_id: str
    report_id: str
    section_id: str
    source_type: str
    source_id: str
    finding_id: str = ""
    evidence_id: str = ""
    risk_factor_id: str = ""
    generated_by: str = "TrustNarrativeEngine"
    template_version: str = "1.0.0"
    language: str = "en"

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 46: Narrative Versioning
# ---------------------------------------------------------------------------

class NarrativeVersionDTO(BaseModel):
    narrative_id: str
    schema_version: str = "4.0.0"
    template_version: str = "1.0.0"
    language_version: str = "1.0.0"
    change_reason: str = "INITIAL_GENERATION"

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Validation Result
# ---------------------------------------------------------------------------

class NarrativeValidationDTO(BaseModel):
    validation_id: str
    narrative_id: str
    passed: bool = True
    checks_performed: int = 0
    checks_passed: int = 0
    checks_failed: int = 0
    failures: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Metric
# ---------------------------------------------------------------------------

class NarrativeMetricDTO(BaseModel):
    narratives_generated_total: int = 1
    narratives_failed_total: int = 0
    narratives_validation_failed_total: int = 0
    llm_requests_total: int = 0
    llm_failures_total: int = 0
    llm_fallback_total: int = 0
    generation_duration_ms: float = 0.0
    validation_duration_ms: float = 0.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Full Narrative Document
# ---------------------------------------------------------------------------

class NarrativeDocumentDTO(BaseModel):
    narrative_id: str
    report_id: str
    analysis_id: str
    schema_version: str = "4.0.0"
    template_version: str = "1.0.0"
    language: str = "en"
    mode: str = "DETERMINISTIC_MODE"  # DETERMINISTIC_MODE, LLM_ASSISTED_MODE
    status: str = "COMPLETED"
    executive_summary: ExecutiveSummaryNarrativeDTO
    risk_narrative: RiskNarrativeDTO
    finding_narratives: List[FindingNarrativeDTO] = Field(default_factory=list)
    evidence_narratives: List[EvidenceNarrativeDTO] = Field(default_factory=list)
    contradiction_narratives: List[ContradictionNarrativeDTO] = Field(default_factory=list)
    statements: List[NarrativeStatementDTO] = Field(default_factory=list)
    lineage: List[NarrativeLineageDTO] = Field(default_factory=list)
    technical_summary: str = ""
    user_friendly_summary: str = ""
    analyst_summary: str = ""
    limitations: List[str] = Field(default_factory=list)
    validation: Optional[NarrativeValidationDTO] = None
    generated_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)
