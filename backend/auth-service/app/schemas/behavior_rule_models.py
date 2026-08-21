"""Pydantic v2 DTO Schemas for Enterprise Malware Behavior Pattern & Deterministic Rule Evaluation Engine (Phase 3.9 Part 1A.24).

Strictly typed DTOs for rules, versions, packs, conditions, evaluations, condition results,
execution traces, evidence, suppressions, exceptions, conflicts, summaries, cards, graphs, metrics, and result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class BehaviorRuleConditionDTO(BaseModel):
    condition_id: str
    condition_type: str = "PERMISSION_USED"
    expected: str
    operator: str = "AND"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorRuleDTO(BaseModel):
    rule_id: str
    rule_version: str = "1.0.0"
    namespace: str = "DATAFLOW"  # DATAFLOW, NETWORK, STORAGE, CRYPTOGRAPHY, PERMISSIONS, COMPONENTS, INTENTS, REFLECTION, JNI, WEBVIEW, THIRDPARTY, CREDENTIALS, AUTHENTICATION, PAYMENT, SMS, CONTACTS, LOCATION, MEDIA, DEVICE_IDENTITY, EXECUTION, PERSISTENCE, THREAT_INTELLIGENCE, COMPOSITE
    name: str
    description: str
    status: str = "ACTIVE"  # DRAFT, TESTING, ACTIVE, DISABLED, DEPRECATED, RETIRED
    severity_hint: str = "HIGH"
    confidence_hint: str = "HIGH"
    prerequisites: List[str] = Field(default_factory=list)
    conditions: List[BehaviorRuleConditionDTO] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorRuleVersionDTO(BaseModel):
    rule_id: str
    rule_version: str
    author: str = "TruthShield Core Team"
    status: str = "ACTIVE"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorRulePackDTO(BaseModel):
    pack_id: str
    pack_version: str = "1.0.0"
    rules_count: int = 0
    checksum: str = "sha256_mock_checksum"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleConditionResultDTO(BaseModel):
    condition_id: str
    condition_type: str
    expected: str
    actual: str
    matched: bool = True
    confidence: str = "HIGH"
    reason: str = "Matched expected criteria"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleExecutionTraceDTO(BaseModel):
    trace_id: str
    rule_id: str
    rule_version: str
    duration_ms: int = 0
    condition_results: List[RuleConditionResultDTO] = Field(default_factory=list)
    final_state: str = "MATCHED"
    confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorRuleEvaluationDTO(BaseModel):
    evaluation_id: str
    rule_id: str
    rule_version: str
    namespace: str
    state: str = "MATCHED"  # MATCHED, NOT_MATCHED, PARTIALLY_MATCHED, NOT_EVALUABLE, INSUFFICIENT_EVIDENCE, SUPPRESSED, EXCEPTION_APPLIED, CONFLICTED, ERROR, UNKNOWN
    confidence: str = "HIGH"
    evidence_provenance: str = "Direct Technical Evidence"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleEvidenceDTO(BaseModel):
    evidence_id: str
    rule_id: str
    evidence_type: str
    source_module: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleSuppressionDTO(BaseModel):
    suppression_id: str
    rule_id: str
    reason: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleExceptionDTO(BaseModel):
    exception_id: str
    rule_id: str
    scope: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleConflictDTO(BaseModel):
    conflict_id: str
    rule_a_id: str
    rule_b_id: str
    reason: str = "Contradictory execution paths"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleSummaryDTO(BaseModel):
    title: str
    summary_text: str
    matched_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleCardDTO(BaseModel):
    card_id: str
    title: str
    rule_id: str
    state: str = "MATCHED"
    confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleGraphDTO(BaseModel):
    nodes_count: int = 0
    edges_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleMetricsDTO(BaseModel):
    rules_loaded: int = 0
    rules_evaluated: int = 0
    rules_matched: int = 0
    rules_partially_matched: int = 0
    rules_not_evaluable: int = 0
    rules_suppressed: int = 0
    rules_conflicted: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RuleResultDTO(BaseModel):
    evaluations: List[BehaviorRuleEvaluationDTO] = Field(default_factory=list)
    traces: List[RuleExecutionTraceDTO] = Field(default_factory=list)
    evidence: List[RuleEvidenceDTO] = Field(default_factory=list)
    suppressions: List[RuleSuppressionDTO] = Field(default_factory=list)
    exceptions: List[RuleExceptionDTO] = Field(default_factory=list)
    conflicts: List[RuleConflictDTO] = Field(default_factory=list)
    rules: List[BehaviorRuleDTO] = Field(default_factory=list)
    packs: List[BehaviorRulePackDTO] = Field(default_factory=list)
    summaries: List[RuleSummaryDTO] = Field(default_factory=list)
    cards: List[RuleCardDTO] = Field(default_factory=list)
    rule_graph: RuleGraphDTO = Field(default_factory=RuleGraphDTO)
    metrics: RuleMetricsDTO = Field(default_factory=RuleMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    analysis_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
