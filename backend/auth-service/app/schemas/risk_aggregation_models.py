"""Pydantic v2 DTO Schemas for Enterprise Risk Aggregation & Cybersecurity Decision Engine (Phase 3.9 Part 1B).

Strictly typed DTOs for risk assessments, risk factors, category scores, contributions, interactions,
mitigations, protective factors, contradictions, audit records, policy versions, decision records,
metrics, explanations, summaries, cards, and assessment result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class RiskAssessmentDTO(BaseModel):
    assessment_id: str
    risk_score: float = 0.0  # Range: 0 - 100
    risk_band: str = "TRUSTED"  # TRUSTED, LOW_RISK, MODERATE_RISK, HIGH_RISK, CRITICAL_RISK
    confidence_level: str = "HIGH"  # VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW, UNKNOWN
    evidence_sufficiency: str = "SUFFICIENT"  # SUFFICIENT, LIMITED, INSUFFICIENT
    decision_state: str = "TRUSTED"  # TRUSTED, LOW_RISK, MODERATE_RISK, HIGH_RISK, CRITICAL_RISK, INSUFFICIENT_EVIDENCE, CONFLICTED_ASSESSMENT, ANALYSIS_ERROR
    primary_risk_category: str = "NETWORK_THREAT"
    risk_factor_count: int = 0
    supporting_finding_count: int = 0
    contradictory_finding_count: int = 0
    mitigating_factor_count: int = 0
    protective_factor_count: int = 0
    uncertainty_count: int = 0
    engine_version: str = "1.0.0"
    configuration_version: str = "1.0.0"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskFactorDTO(BaseModel):
    factor_id: str
    category: str = "NETWORK_THREAT"  # 29 categories
    name: str
    description: str
    base_contribution: float = 10.0
    final_contribution: float = 10.0
    confidence: str = "HIGH"
    evidence_sufficiency: str = "SUFFICIENT"
    reason: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskCategoryScoreDTO(BaseModel):
    category: str
    raw_score: float = 0.0
    normalized_score: float = 0.0
    risk_band: str = "LOW_RISK"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskContributionDTO(BaseModel):
    finding_id: str
    category: str
    contribution_weight: float = 5.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskInteractionDTO(BaseModel):
    interaction_id: str
    factor_a_id: str
    factor_b_id: str
    amplification_bonus: float = 5.0
    description: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskMitigationDTO(BaseModel):
    mitigation_id: str
    description: str
    reduction_amount: float = 5.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskProtectiveFactorDTO(BaseModel):
    protective_id: str
    description: str
    reduction_amount: float = 5.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskContradictionDTO(BaseModel):
    contradiction_id: str
    description: str
    uncertainty_penalty: float = 2.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskAuditRecordDTO(BaseModel):
    audit_id: str
    policy_version: str = "1.0.0"
    configuration_checksum: str = "sha256_mock_checksum"
    audit_trail_text: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskPolicyVersionDTO(BaseModel):
    policy_version: str = "1.0.0"
    author: str = "TruthShield Core Policy Engine"
    description: str = "Standard Enterprise Cybersecurity Risk Policy v1.0.0"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskDecisionRecordDTO(BaseModel):
    decision_id: str
    decision_state: str = "TRUSTED"
    recommendation: str = "ANALYSIS_COMPLETE"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskMetricsDTO(BaseModel):
    assessments_evaluated: int = 1
    high_risk_assessments: int = 0
    critical_risk_assessments: int = 0
    insufficient_evidence_assessments: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskExplanationDTO(BaseModel):
    explanation_id: str
    summary_text: str
    primary_reasons: List[str] = Field(default_factory=list)
    mitigating_reasons: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskSummaryDTO(BaseModel):
    title: str
    risk_score: float = 0.0
    risk_band: str = "TRUSTED"
    confidence_level: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskCardDTO(BaseModel):
    card_id: str
    category: str
    score: float = 0.0
    risk_band: str = "LOW_RISK"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskAssessmentResultDTO(BaseModel):
    assessment: RiskAssessmentDTO
    factors: List[RiskFactorDTO] = Field(default_factory=list)
    category_scores: List[RiskCategoryScoreDTO] = Field(default_factory=list)
    contributions: List[RiskContributionDTO] = Field(default_factory=list)
    interactions: List[RiskInteractionDTO] = Field(default_factory=list)
    mitigations: List[RiskMitigationDTO] = Field(default_factory=list)
    protective_factors: List[RiskProtectiveFactorDTO] = Field(default_factory=list)
    contradictions: List[RiskContradictionDTO] = Field(default_factory=list)
    audit_record: RiskAuditRecordDTO
    policy_version: RiskPolicyVersionDTO
    decision_record: RiskDecisionRecordDTO
    metrics: RiskMetricsDTO
    explanation: RiskExplanationDTO
    summary: RiskSummaryDTO
    cards: List[RiskCardDTO] = Field(default_factory=list)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    calculation_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
