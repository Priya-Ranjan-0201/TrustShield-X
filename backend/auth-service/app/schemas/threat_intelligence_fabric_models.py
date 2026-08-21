"""
TruthShield X — Threat Intelligence Fabric & Collaborative Defense Models (Phase 22).

Strictly typed Pydantic models for Intelligence Sources, Feeds, Normalized Objects,
Threat Graph Nodes/Edges, Campaign Discovery & Evolution, Local Relevance, Early Warnings,
Forecasting & Calibration, Collaborative Defense, Privacy/Redaction, and Quality Metrics.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 22)
# ============================================================================

IntelligenceSourceTypeLiteral = Literal[
    "INTERNAL",
    "COMMERCIAL",
    "GOVERNMENT",
    "COMMUNITY",
    "ISAC_ISAO",
    "OPEN_SOURCE",
    "PARTNER",
    "SENSOR",
    "INCIDENT_DERIVED",
    "AI_DERIVED",
]

IntelligenceClassificationLiteral = Literal[
    "PRIVATE",
    "TENANT_INTERNAL",
    "PARTNER",
    "COMMUNITY",
    "RESTRICTED",
    "PUBLIC",
]

IntelligenceStatusLiteral = Literal[
    "NEW",
    "VALIDATED",
    "ACTIVE",
    "AGING",
    "STALE",
    "EXPIRED",
    "REVOKED",
    "CONFLICTING",
]

AttributionConfidenceLiteral = Literal[
    "POSSIBLE",
    "SUSPECTED",
    "ASSESSED",
    "HIGH_CONFIDENCE_ASSESSMENT",
    "VERIFIED",
    "UNCERTAIN",
]

CampaignLifecycleLiteral = Literal[
    "DISCOVERED",
    "ASSESSED",
    "ACTIVE",
    "EXPANDING",
    "DECLINING",
    "DORMANT",
    "CONCLUDED",
    "DISPUTED",
]

ThreatGraphEdgeTypeLiteral = Literal[
    "ASSOCIATED_WITH",
    "RESOLVES_TO",
    "HOSTED_ON",
    "USES",
    "TARGETS",
    "DELIVERS",
    "EXPLOITS",
    "OBSERVED_IN",
    "RELATED_TO",
    "PART_OF",
    "DERIVED_FROM",
    "CORROBORATED_BY",
    "CONTRADICTED_BY",
]


# ============================================================================
# Source & Feed Health DTOs
# ============================================================================

class IntelligenceSourceDTO(BaseModel):
    source_id: str = Field(default_factory=lambda: f"src_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    name: str
    type: IntelligenceSourceTypeLiteral = "COMMERCIAL"
    reliability: Literal["VERY_HIGH", "HIGH", "MEDIUM", "LOW", "UNRELIABLE"] = "HIGH"
    trust_level: float = Field(default=0.90, ge=0.0, le=1.0)
    format: Literal["STIX2", "TAXII2", "MISP_JSON", "CSV", "TELEMETRY"] = "STIX2"
    ingestion_method: Literal["API_POLL", "WEBHOOK", "STREAM", "MANUAL"] = "API_POLL"
    update_frequency_minutes: int = 15
    status: Literal["ACTIVE", "DEGRADED", "FAILED", "STALE", "DISABLED"] = "ACTIVE"
    last_successful_ingestion: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_failed_ingestion: Optional[str] = None
    classification: IntelligenceClassificationLiteral = "PARTNER"

    model_config = ConfigDict(frozen=True)


class FeedHealthDTO(BaseModel):
    feed_id: str
    availability_pct: float = 99.8
    ingestion_success_rate_pct: float = 99.5
    latency_ms: float = 120.0
    freshness_state: Literal["CURRENT", "STALE", "EXPIRED", "UNKNOWN"] = "CURRENT"
    schema_errors_count: int = 0
    duplicate_rate_pct: float = 1.2
    rejection_rate_pct: float = 0.5
    object_volume: int = 42500
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Intelligence Object & Graph DTOs
# ============================================================================

class ThreatIntelligenceObjectDTO(BaseModel):
    object_id: str = Field(default_factory=lambda: f"tio_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    object_type: Literal[
        "IP", "DOMAIN", "URL", "HASH", "FILE", "CERTIFICATE",
        "EMAIL", "ACCOUNT", "INFRASTRUCTURE", "MALWARE", "TOOL",
        "TECHNIQUE", "ACTOR", "CAMPAIGN", "VULNERABILITY", "BEHAVIOR",
        "TACTIC", "INDICATOR"
    ]
    value: str
    canonical_value: str
    source_id: str
    collection_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    observation_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ingestion_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    confidence: float = Field(default=0.88, ge=0.0, le=1.0)
    status: IntelligenceStatusLiteral = "ACTIVE"
    classification: IntelligenceClassificationLiteral = "COMMUNITY"
    content_hash: str = Field(default_factory=lambda: f"sha256_{uuid.uuid4().hex}")
    version: int = 1
    decay_score: float = Field(default=1.0, ge=0.0, le=1.0)

    model_config = ConfigDict(frozen=True)


class ThreatGraphNodeDTO(BaseModel):
    node_id: str
    node_type: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class ThreatGraphEdgeDTO(BaseModel):
    edge_id: str = Field(default_factory=lambda: f"edge_{uuid.uuid4().hex[:8]}")
    source_node_id: str
    target_node_id: str
    relationship_type: ThreatGraphEdgeTypeLiteral
    confidence: float = 0.90
    evidence_ids: List[str] = Field(default_factory=list)
    source_id: str = "src_graph"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class ThreatIntelligenceGraphDTO(BaseModel):
    graph_id: str = Field(default_factory=lambda: f"tig_{uuid.uuid4().hex[:8]}")
    nodes: List[ThreatGraphNodeDTO] = Field(default_factory=list)
    edges: List[ThreatGraphEdgeDTO] = Field(default_factory=list)
    max_depth_limit: int = 5

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Campaign Discovery, Local Relevance & Early Warnings
# ============================================================================

class CampaignClusterDTO(BaseModel):
    campaign_id: str = Field(default_factory=lambda: f"camp_{uuid.uuid4().hex[:8]}")
    name: str
    lifecycle: CampaignLifecycleLiteral = "ACTIVE"
    confidence: float = Field(default=0.92, ge=0.0, le=1.0)
    attribution: str = "UNKNOWN_THREAT_GROUP"
    attribution_confidence: AttributionConfidenceLiteral = "UNCERTAIN"
    infrastructure: List[str] = Field(default_factory=list)
    indicators: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=list)
    targeted_sectors: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evolution_log: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class LocalThreatRelevanceDTO(BaseModel):
    tenant_id: str
    threat_entity_id: str
    technical_relevance_score: float = Field(default=85.0, ge=0.0, le=100.0)
    exposure_relevance_score: float = Field(default=75.0, ge=0.0, le=100.0)
    threat_activity_score: float = Field(default=90.0, ge=0.0, le=100.0)
    overall_relevance_score: float = Field(default=83.5, ge=0.0, le=100.0)
    affected_local_assets: List[str] = Field(default_factory=list)
    recommended_defensive_action: str = "TIGHTEN_WAF_RULES_AND_SIMULATE_CONTAINMENT"

    model_config = ConfigDict(frozen=True)


class ThreatEarlyWarningDTO(BaseModel):
    warning_id: str = Field(default_factory=lambda: f"warn_{uuid.uuid4().hex[:8]}")
    threat_title: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    confidence: float = Field(default=0.89, ge=0.0, le=1.0)
    local_relevance_score: float = 85.0
    affected_assets: List[str] = Field(default_factory=list)
    early_warning_signals: List[str] = Field(default_factory=list)
    is_confirmed: bool = False
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class ThreatForecastDTO(BaseModel):
    forecast_id: str = Field(default_factory=lambda: f"fc_{uuid.uuid4().hex[:8]}")
    threat_actor_or_campaign: str
    predicted_growth_rate_pct: float = 14.5
    predicted_target_overlap_pct: float = 22.0
    confidence_interval: str = "82% - 94%"
    input_period_days: int = 30
    status: Literal["PREDICTED", "NOT_ENOUGH_DATA"] = "PREDICTED"
    calibration_accuracy_pct: float = 91.2
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Collaborative Defense, Disputes & Quality Metrics
# ============================================================================

class CollaborativeContributionDTO(BaseModel):
    contribution_id: str = Field(default_factory=lambda: f"contrib_{uuid.uuid4().hex[:8]}")
    tenant_id: str
    contributor_identity: str
    object_value: str
    classification: IntelligenceClassificationLiteral = "COMMUNITY"
    is_redacted: bool = True
    content_hash: str = Field(default_factory=lambda: f"sha256_{uuid.uuid4().hex}")
    submitted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class IntelligenceDisputeDTO(BaseModel):
    dispute_id: str = Field(default_factory=lambda: f"disp_{uuid.uuid4().hex[:8]}")
    object_id: str
    disputing_tenant_id: str
    reason: str
    dispute_status: Literal["OPEN", "UNDER_REVIEW", "RESOLVED", "REJECTED"] = "OPEN"
    submitted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class IntelligenceRevocationDTO(BaseModel):
    revocation_id: str = Field(default_factory=lambda: f"rev_{uuid.uuid4().hex[:8]}")
    object_id: str
    reason: str
    affected_indicators: List[str] = Field(default_factory=list)
    affected_campaigns: List[str] = Field(default_factory=list)
    affected_detections: List[str] = Field(default_factory=list)
    affected_incidents: List[str] = Field(default_factory=list)
    revoked_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class IntelligenceQualityMetricsDTO(BaseModel):
    completeness_score: float = 95.0
    freshness_score: float = 98.2
    provenance_integrity_pct: float = 100.0
    consistency_score: float = 94.0
    corroboration_rate_pct: float = 91.5
    overall_quality_grade: str = "GRADE_A"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
