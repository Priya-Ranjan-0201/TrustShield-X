"""Pydantic v2 DTO Schemas for Unified Trust Intelligence Graph (Phase 4.0 Part 5).

Strictly typed DTOs for Canonical Entities, Graph Relationships, Evidence Bindings,
Correlation Candidates, Threat Campaigns, Attack Chains, Threat Actor Associations,
Graph Versions, Snapshots, Diffs, Review Queues, and Search/Query interfaces.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Section 2 & 3: Canonical Entity DTOs
# ---------------------------------------------------------------------------

class EntityObservationDTO(BaseModel):
    observation_id: str
    entity_id: str
    source_analysis_id: str
    source_module: str
    raw_value: str
    observed_at: str
    context_data: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EntityResolutionRecordDTO(BaseModel):
    record_id: str
    entity_id: str
    target_entity_id: Optional[str] = None
    resolution_state: str = "EXACT_MATCH"  # EXACT_MATCH, STRONG_MATCH, PROBABLE_MATCH, etc.
    confidence: str = "HIGH"
    resolution_method: str = "EXACT_IDENTIFIER"
    signals_used: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CanonicalEntityDTO(BaseModel):
    entity_id: str
    entity_type: str  # DOMAIN, URL, IP_ADDRESS, CERTIFICATE, HASH, PACKAGE, PHONE, UPI_ID, etc.
    canonical_value: str
    display_value: str
    normalized_value: str
    value_hash: str
    source_count: int = 1
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    confidence: str = "HIGH"  # VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW, UNKNOWN
    resolution_status: str = "EXACT_MATCH"
    privacy_classification: str = "PUBLIC"  # PUBLIC, INTERNAL, RESTRICTED, HIGHLY_SENSITIVE
    organization_id: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CanonicalEntityCreateDTO(BaseModel):
    entity_type: str
    raw_value: str
    source_analysis_id: str
    source_module: str
    confidence: str = "HIGH"
    privacy_classification: Optional[str] = None
    organization_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Section 11-17: Graph Relationship & Correlation DTOs
# ---------------------------------------------------------------------------

class RelationshipEvidenceDTO(BaseModel):
    evidence_binding_id: str
    relationship_id: str
    evidence_id: str
    finding_id: Optional[str] = None
    analysis_id: str
    evidence_strength: str = "DIRECT"  # DIRECT, CORROBORATED, INDIRECT, WEAK
    observation_summary: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CorrelationCandidateDTO(BaseModel):
    candidate_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    candidate_score: float = 0.0
    confidence: str = "MEDIUM"
    evidence_count: int = 1
    correlation_method: str = "NORMALIZED_IDENTIFIER"
    false_correlation_penalty: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class GraphRelationshipDTO(BaseModel):
    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str  # HOSTS, RESOLVES_TO, COMMUNICATES_WITH, USES_CERTIFICATE, etc.
    confidence: str = "HIGH"  # VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW, UNKNOWN
    evidence_strength: str = "STRONG"
    resolution_status: str = "ACTIVE"  # ACTIVE, WEAK, STALE, CONFLICTED, REVOKED, UNRESOLVED
    correlation_method: str = "EXACT_IDENTIFIER"
    correlation_version: str = "1.0.0"
    first_observed: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_observed: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_count: int = 1
    evidence_ids: List[str] = Field(default_factory=list)
    finding_ids: List[str] = Field(default_factory=list)
    analysis_ids: List[str] = Field(default_factory=list)
    provenance_ids: List[str] = Field(default_factory=list)
    status: str = "ACTIVE"
    is_manual: bool = False
    author_id: Optional[str] = None
    staleness_reason: Optional[str] = None
    conflicting_sources: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 24-34: Threat Campaign & Attack Chain DTOs
# ---------------------------------------------------------------------------

class ThreatCampaignDTO(BaseModel):
    campaign_id: str
    name: str
    campaign_type: str  # PHISHING_CAMPAIGN, MALWARE_CAMPAIGN, FINANCIAL_FRAUD_CAMPAIGN, etc.
    status: str = "ACTIVE"
    confidence: str = "HIGH"
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    entity_count: int = 0
    analysis_count: int = 0
    finding_count: int = 0
    evidence_count: int = 0
    relationship_count: int = 0
    threat_actor: str = "UNKNOWN"
    threat_actor_confidence: str = "UNCONFIRMED_ASSOCIATION"
    entities: List[str] = Field(default_factory=list)
    attack_chain_ids: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class AttackChainStepDTO(BaseModel):
    step_id: str
    chain_id: str
    step_number: int
    stage: str  # ENTRY_POINT, EXECUTION, COLLECTION, TRANSMISSION, IMPACT
    title: str
    description: str
    step_state: str = "CONFIRMED_STEP"  # CONFIRMED_STEP, SUPPORTED_STEP, POSSIBLE_STEP, MISSING_STEP, CONTRADICTED_STEP
    confidence: str = "HIGH"
    entity_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    finding_ids: List[str] = Field(default_factory=list)
    missing_evidence_note: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class AttackChainDTO(BaseModel):
    chain_id: str
    case_id: Optional[str] = None
    campaign_id: Optional[str] = None
    title: str
    entry_point: str
    confidence: str = "HIGH"
    status: str = "ACTIVE"
    steps: List[AttackChainStepDTO] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    finding_ids: List[str] = Field(default_factory=list)
    missing_steps_count: int = 0
    uncertainty_summary: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatActorAssociationDTO(BaseModel):
    association_id: str
    actor_name: str
    campaign_id: str
    confidence: str = "LOW"
    source: str = "THREAT_INTEL"
    evidence: str = ""
    attribution_type: str = "UNCONFIRMED_ASSOCIATION"  # EXPLICIT_SOURCE_ATTRIBUTION, ANALYST_ATTRIBUTION, etc.
    attribution_status: str = "UNCONFIRMED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 43-45: Graph Versioning & Snapshot DTOs
# ---------------------------------------------------------------------------

class GraphVersionDTO(BaseModel):
    graph_version_id: str
    case_id: Optional[str] = None
    version_number: int = 1
    schema_version: str = "4.0.0"
    correlation_version: str = "1.0.0"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = "SYSTEM"
    change_summary: str = "Initial graph construction"
    content_hash: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class GraphSnapshotDTO(BaseModel):
    snapshot_id: str
    graph_version_id: str
    case_id: Optional[str] = None
    nodes: List[CanonicalEntityDTO] = Field(default_factory=list)
    edges: List[GraphRelationshipDTO] = Field(default_factory=list)
    campaigns: List[ThreatCampaignDTO] = Field(default_factory=list)
    attack_chains: List[AttackChainDTO] = Field(default_factory=list)
    total_nodes: int = 0
    total_edges: int = 0
    content_hash: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class GraphDiffDTO(BaseModel):
    base_version: int
    target_version: int
    added_entity_ids: List[str] = Field(default_factory=list)
    removed_entity_ids: List[str] = Field(default_factory=list)
    added_relationship_ids: List[str] = Field(default_factory=list)
    removed_relationship_ids: List[str] = Field(default_factory=list)
    changed_confidence_relationships: Dict[str, str] = Field(default_factory=dict)
    changed_campaigns: List[str] = Field(default_factory=list)
    changed_attack_chains: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 49, 79-83: Correlation Run, Review Queue & Analyst Operations
# ---------------------------------------------------------------------------

class CorrelationRunDTO(BaseModel):
    run_id: str
    case_id: Optional[str] = None
    analysis_scope: List[str] = Field(default_factory=list)
    correlation_version: str = "1.0.0"
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    status: str = "RUNNING"  # RUNNING, COMPLETED, FAILED
    candidate_count: int = 0
    accepted_count: int = 0
    rejected_count: int = 0
    uncertain_count: int = 0
    error_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CorrelationReviewItemDTO(BaseModel):
    review_id: str
    relationship_id: str
    source_entity_value: str
    target_entity_value: str
    relationship_type: str
    confidence: str
    flag_reason: str  # LOW_CONFIDENCE, CONFLICT, HIGH_IMPACT_CAMPAIGN, POTENTIAL_FALSE_POSITIVE, STALE
    priority: str = "MEDIUM"
    status: str = "PENDING"  # PENDING, CONFIRMED, REJECTED, SUPPRESSED
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ManualCorrelationCreateDTO(BaseModel):
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    confidence: str = "MEDIUM"
    reason: str
    evidence_ids: List[str] = Field(default_factory=list)
    expiration_days: Optional[int] = 30


class RelationshipReviewActionDTO(BaseModel):
    action: str  # CONFIRM, REJECT, FLAG_FOR_REVIEW, MARK_STALE, MARK_CONFLICTED
    reviewer_note: str = ""


# ---------------------------------------------------------------------------
# Section 58-61: Query, Search & Graph API Responses
# ---------------------------------------------------------------------------

class GraphQueryParamsDTO(BaseModel):
    entity_id: Optional[str] = None
    depth: int = 1
    entity_types: Optional[List[str]] = None
    relationship_types: Optional[List[str]] = None
    min_confidence: Optional[str] = None
    status: Optional[str] = None
    limit: int = 100
    include_provenance: bool = True
    include_evidence: bool = True


class UnifiedGraphResponseDTO(BaseModel):
    graph_version: int = 1
    total_nodes: int = 0
    total_edges: int = 0
    nodes: List[CanonicalEntityDTO] = Field(default_factory=list)
    edges: List[GraphRelationshipDTO] = Field(default_factory=list)
    campaigns: List[ThreatCampaignDTO] = Field(default_factory=list)
    attack_chains: List[AttackChainDTO] = Field(default_factory=list)
    truncated: bool = False
    query_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


class GraphSearchRequestDTO(BaseModel):
    query: str
    entity_types: Optional[List[str]] = None
    limit: int = 50


class GraphSearchResultDTO(BaseModel):
    entity_id: str
    entity_type: str
    display_value: str
    canonical_value: str
    confidence: str
    match_field: str
    source_count: int
    first_seen: str
    last_seen: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class GraphSearchResponseDTO(BaseModel):
    query: str
    results: List[GraphSearchResultDTO] = Field(default_factory=list)
    total_results: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CorrelationExplanationDTO(BaseModel):
    relationship_id: str
    source_entity: str
    target_entity: str
    relationship_type: str
    confidence: str
    why_connected: str
    evidence_signals: List[str] = Field(default_factory=list)
    correlation_rule: str
    rule_version: str
    false_correlation_risk: str
    unresolved_questions: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)
