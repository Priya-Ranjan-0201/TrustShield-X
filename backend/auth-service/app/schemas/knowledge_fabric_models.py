"""Pydantic v2 DTO Schemas for Digital Trust Knowledge Fabric, Security Reasoning & Investigator Copilot (Phase 7).

Strictly typed DTOs for Knowledge Objects, Relationships, Evidence Lineage, Knowledge Versioning,
Snapshots, Diffs, Knowledge Conflicts, Security Reasoning Results, Digital Trust Scores & Profiles,
Investigation Sessions, Attack Stories, Investigation Recommendations, Case Briefs, and Investigator Copilot.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Sections 3, 4, 12, 17)
# ============================================================================

KnowledgeObjectTypeLiteral = Literal[
    "ENTITY",
    "EVIDENCE",
    "INCIDENT",
    "CAMPAIGN",
    "PREDICTION",
    "THREAT_SIGNAL",
    "RESPONSE",
    "OBSERVATION",
    "REPORT",
    "ACTOR_HYPOTHESIS",
    "ATTACK_PATTERN",
    "TRUST_EVENT",
]

RelationshipTypeLiteral = Literal[
    "SUPPORTS",
    "CONTRADICTS",
    "DERIVED_FROM",
    "OBSERVED_IN",
    "ASSOCIATED_WITH",
    "CAUSED_BY",
    "PRECEDES",
    "FOLLOWS",
    "SIMILAR_TO",
    "PART_OF",
    "RELATED_TO",
    "RESPONDED_BY",
    "VERIFIED_BY",
    "PREDICTS",
    "INVALIDATES",
    "SUPERSEDES",
]

ReasoningStateLiteral = Literal[
    "FACT",
    "VERIFIED",
    "STRONG_INFERENCE",
    "WEAK_INFERENCE",
    "PREDICTION",
    "UNKNOWN",
]

TrustDimensionLiteral = Literal[
    "IDENTITY_TRUST",
    "CONTENT_TRUST",
    "SOURCE_TRUST",
    "INFRASTRUCTURE_TRUST",
    "BEHAVIOR_TRUST",
    "EVIDENCE_TRUST",
]


# ============================================================================
# Section 3 & 4: Knowledge Object & Relationship DTOs
# ============================================================================

class KnowledgeObjectDTO(BaseModel):
    knowledge_object_id: str = Field(default_factory=lambda: f"kobj_{uuid.uuid4().hex[:12]}")
    object_type: KnowledgeObjectTypeLiteral
    canonical_reference: str
    tenant_id: str = "default_tenant"
    classification: str = "RESTRICTED"  # PUBLIC, INTERNAL, RESTRICTED, CONFIDENTIAL
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    provenance: Dict[str, Any] = Field(default_factory=dict)
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class KnowledgeRelationshipDTO(BaseModel):
    relationship_id: str = Field(default_factory=lambda: f"krel_{uuid.uuid4().hex[:12]}")
    source_id: str
    target_id: str
    relationship_type: RelationshipTypeLiteral
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    evidence_ids: List[str] = Field(default_factory=list)
    causality_verified: bool = False  # Strictly False unless causality is established
    tenant_id: str = "default_tenant"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 5 & 6: Evidence Provenance & Lineage DTOs
# ============================================================================

class EvidenceLineageDTO(BaseModel):
    lineage_id: str = Field(default_factory=lambda: f"lin_{uuid.uuid4().hex[:12]}")
    knowledge_object_id: str
    original_artifact_id: str
    extraction_module: str
    detector_id: str
    detector_version: str = "1.0.0"
    algorithm_version: str = "1.0.0"
    transformation_steps: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    source: str = "CANONICAL_DETECTOR"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EvidenceChainDTO(BaseModel):
    conclusion_id: str
    chain_elements: List[Dict[str, Any]] = Field(default_factory=list)
    root_artifacts: List[str] = Field(default_factory=list)
    verified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Section 7, 8, 9: Versioning, Snapshots, and Knowledge Diffs
# ============================================================================

class KnowledgeVersionDTO(BaseModel):
    version_id: str = Field(default_factory=lambda: f"kver_{uuid.uuid4().hex[:12]}")
    knowledge_object_id: str
    version: int
    previous_version: Optional[int] = None
    changed_fields: List[str] = Field(default_factory=list)
    change_reason: str
    changed_by: str
    snapshot_data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class KnowledgeSnapshotDTO(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"ksnap_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    label: str
    snapshot_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    object_count: int = 0
    relationship_count: int = 0
    objects: Dict[str, Any] = Field(default_factory=dict)
    relationships: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class KnowledgeDiffDTO(BaseModel):
    diff_id: str = Field(default_factory=lambda: f"kdiff_{uuid.uuid4().hex[:12]}")
    snapshot_a_id: str
    snapshot_b_id: str
    new_evidence: List[str] = Field(default_factory=list)
    removed_evidence: List[str] = Field(default_factory=list)
    changed_confidence: List[Dict[str, Any]] = Field(default_factory=list)
    new_relationships: List[Dict[str, Any]] = Field(default_factory=list)
    removed_relationships: List[Dict[str, Any]] = Field(default_factory=list)
    new_campaigns: List[str] = Field(default_factory=list)
    changed_risk: List[Dict[str, Any]] = Field(default_factory=list)
    changed_predictions: List[Dict[str, Any]] = Field(default_factory=list)
    summary: str = "No changes detected."

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 10 - 15: Security Reasoning Engine & Conflict Models
# ============================================================================

class ReasoningResultDTO(BaseModel):
    reasoning_id: str = Field(default_factory=lambda: f"rsn_{uuid.uuid4().hex[:12]}")
    question: str
    conclusion: str
    reasoning_state: ReasoningStateLiteral = "VERIFIED"
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    evidence_ids: List[str] = Field(default_factory=list)
    supporting_signals: List[str] = Field(default_factory=list)
    counter_evidence_ids: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    uncertainty: str = "LOW"
    knowledge_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    engine_version: str = "7.0.0"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class KnowledgeConflictDTO(BaseModel):
    conflict_id: str = Field(default_factory=lambda: f"cnfl_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    entity_or_object_id: str
    conflict_type: str  # e.g., "CONFIDENCE_MISMATCH", "VERDICT_CONTRADICTION", "TEMPORAL_INCONSISTENCY"
    description: str
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    contradicting_evidence_ids: List[str] = Field(default_factory=list)
    resolution_status: str = "UNRESOLVED"  # UNRESOLVED, RESOLVED_PRECEDENCE, RESOLVED_MANUAL
    resolution_rationale: Optional[str] = None
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 16 - 20: Digital Trust Score & Profiles
# ============================================================================

class DigitalTrustScoreDTO(BaseModel):
    trust_score: float = Field(default=80.0, ge=0.0, le=100.0)
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    factors: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    decay_applied: bool = False
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DigitalTrustProfileDTO(BaseModel):
    profile_id: str = Field(default_factory=lambda: f"tprof_{uuid.uuid4().hex[:12]}")
    entity_id: str
    tenant_id: str = "default_tenant"
    trust_score: float = Field(default=80.0, ge=0.0, le=100.0)
    risk_score: float = Field(default=20.0, ge=0.0, le=100.0)
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    associated_campaigns: List[str] = Field(default_factory=list)
    recent_incidents: List[str] = Field(default_factory=list)
    predictions: List[Dict[str, Any]] = Field(default_factory=list)
    trust_history: List[Dict[str, Any]] = Field(default_factory=list)
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 22 - 26: Investigator Copilot DTOs
# ============================================================================

class CopilotCitationDTO(BaseModel):
    citation_id: str = Field(default_factory=lambda: f"cit_{uuid.uuid4().hex[:8]}")
    citation_type: str  # EVIDENCE, ENTITY, INCIDENT, CAMPAIGN, REPORT
    target_id: str
    title: str
    snippet: str
    confidence: float = 0.90
    uri: Optional[str] = None


class CopilotQueryRequestDTO(BaseModel):
    query: str
    session_id: Optional[str] = None
    investigation_id: Optional[str] = None
    context_filters: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: str = "default_tenant"


class CopilotResponseDTO(BaseModel):
    response_id: str = Field(default_factory=lambda: f"cresp_{uuid.uuid4().hex[:12]}")
    query: str
    answer: str
    confidence: float = 0.90
    citations: List[CopilotCitationDTO] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    uncertainty_declaration: Optional[str] = None
    recommended_next_steps: List[str] = Field(default_factory=list)
    knowledge_snapshot_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    model_governance: Dict[str, Any] = Field(default_factory=dict)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Section 27 - 35: Investigation Workspace, Attack Story & Case Brief
# ============================================================================

class AttackStoryStageDTO(BaseModel):
    stage_name: str  # INITIAL_OBSERVATION, FIRST_SUSPICIOUS_ACTIVITY, CORRELATION, CAMPAIGN_DISCOVERY, ESCALATION, RESPONSE, VERIFICATION
    timestamp: str
    description: str
    evidence_ids: List[str] = Field(default_factory=list)
    is_gap: bool = False


class AttackStoryDTO(BaseModel):
    story_id: str = Field(default_factory=lambda: f"story_{uuid.uuid4().hex[:12]}")
    title: str
    incident_or_campaign_id: str
    stages: List[AttackStoryStageDTO] = Field(default_factory=list)
    summary: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class InvestigationRecommendationDTO(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"irec_{uuid.uuid4().hex[:12]}")
    investigation_id: str
    action_title: str
    rationale: str
    information_gain_score: float = Field(default=0.80, ge=0.0, le=1.0)
    effort_estimate: str = "LOW"  # LOW, MEDIUM, HIGH
    bounded_query: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CaseBriefDTO(BaseModel):
    case_brief_id: str = Field(default_factory=lambda: f"cbrief_{uuid.uuid4().hex[:12]}")
    investigation_id: str
    executive_summary: str
    current_risk_score: float
    trust_assessment: Dict[str, Any]
    campaign_association: Optional[str]
    timeline_events_count: int
    key_evidence_ids: List[str]
    counter_evidence_ids: List[str]
    predictions: List[Dict[str, Any]]
    actions_taken: List[Dict[str, Any]]
    action_results: List[Dict[str, Any]]
    open_questions: List[str]
    recommended_next_steps: List[str]
    limitations: List[str]
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class InvestigationSessionDTO(BaseModel):
    investigation_id: str = Field(default_factory=lambda: f"inv_{uuid.uuid4().hex[:12]}")
    title: str
    tenant_id: str = "default_tenant"
    status: str = "ACTIVE"  # ACTIVE, PAUSED, CLOSED
    assigned_analyst: str = "analyst_soc"
    entity_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    incident_ids: List[str] = Field(default_factory=list)
    campaign_ids: List[str] = Field(default_factory=list)
    recommendations: List[InvestigationRecommendationDTO] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
