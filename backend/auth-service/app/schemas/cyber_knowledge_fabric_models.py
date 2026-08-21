"""
TruthShield X — Cyber Knowledge Fabric & Security Reasoning Models (Phase 19).

Strictly typed Pydantic models for Knowledge Objects, Provenance, Temporal Knowledge,
Evidence Graph, Strength Scoring, Contradictions, Security Assertions, Reasoning Traces,
Hypotheses, Gaps, Analogs, Security Memory, Revocation Cascades, Quality Scorecards, and
AI Knowledge Assistant.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 19)
# ============================================================================

KnowledgeObjectTypeLiteral = Literal[
    "ASSET",
    "IDENTITY",
    "USER",
    "SERVICE",
    "APPLICATION",
    "DATASET",
    "DOMAIN",
    "URL",
    "IP",
    "CERTIFICATE",
    "FILE",
    "HASH",
    "VULNERABILITY",
    "CONTROL",
    "POLICY",
    "THREAT",
    "INDICATOR",
    "CAMPAIGN",
    "INCIDENT",
    "ALERT",
    "EVIDENCE",
    "HUNT",
    "PREDICTION",
    "SIMULATION",
    "DEFENSE_ACTION",
    "RECOVERY_EVENT",
    "GOVERNANCE_CONTROL",
    "SECURITY_ASSERTION",
]

KnowledgeRelationTypeLiteral = Literal[
    "OWNS",
    "HOSTS",
    "RUNS",
    "DEPENDS_ON",
    "ACCESSES",
    "PROTECTS",
    "EXPOSES",
    "INDICATES",
    "SUPPORTS",
    "CONTRADICTS",
    "DERIVED_FROM",
    "OBSERVED_IN",
    "RELATED_TO",
    "CORRELATED_WITH",
    "CAUSED",
    "MITIGATED_BY",
    "DETECTED_BY",
    "RESPONDED_BY",
    "SIMULATED_BY",
    "PREDICTED_BY",
    "VERIFIED_BY",
    "REVOKED_BY",
    "REQUIRES",
    "DEPENDS_ON_CONTROL",
    "AFFECTS",
    "RESOLVES",
    "ESCALATES_TO",
]

EpistemicStatusLiteral = Literal[
    "FACT",
    "OBSERVATION",
    "EVIDENCE",
    "CORRELATION",
    "INFERENCE",
    "HYPOTHESIS",
    "PREDICTION",
    "SIMULATION",
    "RECOMMENDATION",
    "DECISION",
]

TemporalStateLiteral = Literal[
    "CURRENT",
    "HISTORICAL",
    "FUTURE_PREDICTED",
    "SIMULATED",
]

AssertionValidationStatusLiteral = Literal[
    "VERIFIED",
    "STRONGLY_SUPPORTED",
    "SUPPORTED",
    "INFERRED",
    "HYPOTHESIS",
    "PREDICTED",
    "SIMULATED",
    "CONFLICTING",
    "UNKNOWN",
    "UNVERIFIED",
    "REVOKED",
]

ConflictStateLiteral = Literal[
    "CONSISTENT",
    "CONFLICTING",
    "INSUFFICIENT_EVIDENCE",
    "UNKNOWN",
    "STALE",
    "REVOKED",
]

FreshnessStateLiteral = Literal[
    "FRESH",
    "AGING",
    "STALE",
    "EXPIRED",
    "UNKNOWN",
]


# ============================================================================
# Core Knowledge Objects & Relationships
# ============================================================================

class KnowledgeObjectDTO(BaseModel):
    object_id: str = Field(default_factory=lambda: f"kobj_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    object_type: KnowledgeObjectTypeLiteral
    canonical_identifier: str
    classification: str = "RESTRICTED"  # PUBLIC, INTERNAL, RESTRICTED, CONFIDENTIAL
    source: str = "TELEMETRY_ENGINE"
    provenance: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    validity_start: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    validity_end: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1
    status: str = "ACTIVE"
    content_hash: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class KnowledgeRelationshipDTO(BaseModel):
    relationship_id: str = Field(default_factory=lambda: f"krel_{uuid.uuid4().hex[:12]}")
    source_id: str
    target_id: str
    relation_type: KnowledgeRelationTypeLiteral
    source: str = "DISCOVERY_ENGINE"
    evidence: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    method: str = "AUTOMATED_CORRELATION"
    actor: str = "SYSTEM_FABRIC"
    version: int = 1
    is_revoked: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class TemporalKnowledgeDTO(BaseModel):
    object_id: str
    temporal_state: TemporalStateLiteral = "CURRENT"
    valid_from: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    valid_until: Optional[str] = None
    observed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class KnowledgeLineageDTO(BaseModel):
    conclusion_id: str
    created_by_model: str = "SecurityReasoningEngine_v1"
    source_data: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    transformations: List[str] = Field(default_factory=list)
    models_used: List[str] = Field(default_factory=list)
    dependent_conclusions: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class KnowledgeDiffDTO(BaseModel):
    diff_id: str = Field(default_factory=lambda: f"diff_{uuid.uuid4().hex[:10]}")
    object_id: str
    old_version: int
    new_version: int
    entity_changes: Dict[str, Any] = Field(default_factory=dict)
    relationship_changes: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_delta: float = 0.0
    status_change: Optional[str] = None

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Evidence Graph, Strength & Contradictions
# ============================================================================

class EvidenceStrengthDTO(BaseModel):
    source_reliability: float = Field(default=0.90, ge=0.0, le=1.0)
    directness: float = Field(default=0.85, ge=0.0, le=1.0)
    freshness: float = Field(default=0.95, ge=0.0, le=1.0)
    corroboration: float = Field(default=0.80, ge=0.0, le=1.0)
    reproducibility: float = Field(default=0.90, ge=0.0, le=1.0)
    integrity: float = Field(default=0.99, ge=0.0, le=1.0)
    independence: float = Field(default=0.85, ge=0.0, le=1.0)
    overall_strength: float = 0.89

    model_config = ConfigDict(frozen=True)


class EvidenceGraphNodeDTO(BaseModel):
    node_id: str
    node_type: str
    label: str
    epistemic_status: EpistemicStatusLiteral = "EVIDENCE"
    confidence: float = 0.90

    model_config = ConfigDict(frozen=True)


class EvidenceGraphEdgeDTO(BaseModel):
    source_id: str
    target_id: str
    relation: Literal["SUPPORTS", "CONTRADICTS", "DERIVED_FROM", "OBSERVED_ON", "ASSOCIATED_WITH"]
    weight: float = 1.0

    model_config = ConfigDict(frozen=True)


class EvidenceGraphDTO(BaseModel):
    nodes: List[EvidenceGraphNodeDTO] = Field(default_factory=list)
    edges: List[EvidenceGraphEdgeDTO] = Field(default_factory=list)
    total_evidence_nodes: int = 0
    contradiction_count: int = 0

    model_config = ConfigDict(frozen=True)


class EvidenceContradictionDTO(BaseModel):
    contradiction_id: str = Field(default_factory=lambda: f"contra_{uuid.uuid4().hex[:10]}")
    entity_id: str
    conflict_type: str
    evidence_a_id: str
    evidence_b_id: str
    description: str
    conflict_state: ConflictStateLiteral = "CONFLICTING"
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Security Assertions & Reasoning Traces
# ============================================================================

class SecurityAssertionDTO(BaseModel):
    assertion_id: str = Field(default_factory=lambda: f"asrt_{uuid.uuid4().hex[:10]}")
    statement: str
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    status: AssertionValidationStatusLiteral = "SUPPORTED"
    epistemic_status: EpistemicStatusLiteral = "INFERENCE"
    provenance: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class SecurityHypothesisDTO(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: f"hypo_{uuid.uuid4().hex[:10]}")
    title: str
    description: str
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.75, ge=0.0, le=1.0)
    rank: int = 1
    is_alternative_explanation: bool = False
    is_ambiguous: bool = False

    model_config = ConfigDict(frozen=True)


class ReasoningTraceDTO(BaseModel):
    conclusion_id: str = Field(default_factory=lambda: f"conc_{uuid.uuid4().hex[:10]}")
    conclusion_statement: str
    supporting_evidence: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    confidence: float = 0.88
    contradictions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    epistemic_status: EpistemicStatusLiteral = "INFERENCE"

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Investigation Questions, Gaps, Analogs & Memory
# ============================================================================

class InvestigationQuestionDTO(BaseModel):
    question_id: str = Field(default_factory=lambda: f"iq_{uuid.uuid4().hex[:8]}")
    question: str
    target_entity: str
    expected_information_gain: float = Field(default=0.85, ge=0.0, le=1.0)
    risk_reduction_impact: float = Field(default=0.80, ge=0.0, le=1.0)
    urgency: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    feasibility: Literal["EASY", "MODERATE", "HARD"] = "EASY"
    priority_score: float = 0.88

    model_config = ConfigDict(frozen=True)


class KnowledgeGapDTO(BaseModel):
    gap_id: str = Field(default_factory=lambda: f"gap_{uuid.uuid4().hex[:8]}")
    gap_type: Literal[
        "MISSING_ASSET_OWNERSHIP",
        "UNKNOWN_DEPENDENCY",
        "MISSING_EVIDENCE",
        "UNKNOWN_IDENTITY",
        "UNKNOWN_CONTROL_STATUS",
        "UNCERTAIN_CAMPAIGN_ASSOCIATION",
    ]
    target_entity: str
    description: str
    security_impact: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    decision_impact: float = 0.85
    uncertainty: float = 0.90
    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"

    model_config = ConfigDict(frozen=True)


class HistoricalAnalogDTO(BaseModel):
    analog_id: str = Field(default_factory=lambda: f"analog_{uuid.uuid4().hex[:8]}")
    past_incident_id: str
    similarity_score: float = Field(default=0.88, ge=0.0, le=1.0)
    matched_techniques: List[str] = Field(default_factory=list)
    context_match: str
    past_response_outcome: str

    model_config = ConfigDict(frozen=True)


class LessonsLearnedDTO(BaseModel):
    lesson_id: str = Field(default_factory=lambda: f"lesson_{uuid.uuid4().hex[:8]}")
    incident_type: str
    successful_defenses: List[str] = Field(default_factory=list)
    failed_defenses: List[str] = Field(default_factory=list)
    recovery_bottlenecks: List[str] = Field(default_factory=list)
    policy_recommendation: str

    model_config = ConfigDict(frozen=True)


class SecurityMemoryRecordDTO(BaseModel):
    memory_id: str = Field(default_factory=lambda: f"mem_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    category: Literal["INCIDENT", "PATTERN", "DEFENSE_OUTCOME", "WEAKNESS", "FALSE_POSITIVE"]
    title: str
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Revocation, Decision Traceability & Quality Scorecard
# ============================================================================

class KnowledgeImpactDTO(BaseModel):
    revocation_id: str = Field(default_factory=lambda: f"rev_{uuid.uuid4().hex[:8]}")
    source_id: str
    affected_assertions: List[str] = Field(default_factory=list)
    affected_incidents: List[str] = Field(default_factory=list)
    affected_reports: List[str] = Field(default_factory=list)
    affected_predictions: List[str] = Field(default_factory=list)
    affected_defenses: List[str] = Field(default_factory=list)
    requires_reassessment: bool = True

    model_config = ConfigDict(frozen=True)


class DecisionTraceabilityDTO(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:10]}")
    decision_type: str
    driving_knowledge: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    governing_policy: str
    alternative_options: List[str] = Field(default_factory=list)
    decision_maker: str
    post_action_outcome: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class KnowledgeQualityScorecardDTO(BaseModel):
    data_quality: float = 92.5
    evidence_quality: float = 94.0
    graph_quality: float = 91.0
    provenance_completeness: float = 98.0
    freshness_score: float = 95.0
    contradiction_rate: float = 2.1
    overall_health_score: float = 93.8

    model_config = ConfigDict(frozen=True)


class SecurityKnowledgeAssistantResponseDTO(BaseModel):
    query: str
    answer: str
    evidence: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.92, ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    unknown_areas: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class CyberKnowledgeFabricSummaryDTO(BaseModel):
    fabric_id: str
    tenant_id: str
    total_knowledge_objects: int
    total_relationships: int
    evidence_nodes_count: int
    active_assertions_count: int
    unresolved_contradictions_count: int
    identified_knowledge_gaps_count: int
    overall_quality_score: float
    last_synthesized: str

    model_config = ConfigDict(frozen=True)
