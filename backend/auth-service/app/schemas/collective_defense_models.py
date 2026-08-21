"""
TruthShield X — Phase 16 Global Threat Intelligence Fusion, Campaign Graph,
Collective Defense Network & Cross-Organization Early Warning Models.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
import hashlib
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Phase 16 Type Literals
# ============================================================================

IntelligenceTypeLiteral = Literal[
    "DOMAIN",
    "URL",
    "IP",
    "CERTIFICATE",
    "FILE_HASH",
    "APK_SIGNATURE",
    "EMAIL_INDICATOR",
    "PHONE_IDENTIFIER",
    "PAYMENT_IDENTIFIER",
    "QR_INDICATOR",
    "VOICE_SIGNATURE",
    "IDENTITY_PATTERN",
    "CAMPAIGN",
    "ATTACK_PATTERN",
    "INFRASTRUCTURE_CLUSTER",
    "BEHAVIORAL_PATTERN",
]

IntelligenceStateLiteral = Literal[
    "OBSERVED",
    "SUBMITTED",
    "VALIDATING",
    "VALIDATED",
    "CORRELATED",
    "SHARED",
    "EXPIRED",
    "REVOKED",
    "DISPUTED",
    "REJECTED",
]

DataClassificationLiteral = Literal[
    "PUBLIC",
    "INTERNAL",
    "SHARED_THREAT_INTELLIGENCE",
    "CONFIDENTIAL",
    "HIGHLY_RESTRICTED",
]

SharingStateLiteral = Literal[
    "PRIVATE",
    "SHARE_PENDING",
    "APPROVED_FOR_SHARING",
    "SHARED",
    "REVOKED",
    "BLOCKED",
]

PrivacyTransformationTypeLiteral = Literal[
    "REDACT",
    "HASH",
    "TOKENIZE",
    "GENERALIZE",
    "AGGREGATE",
    "REMOVE",
]

DisputeStatusLiteral = Literal[
    "OPEN",
    "UNDER_REVIEW",
    "RESOLVED",
    "REJECTED",
]

FreshnessStatusLiteral = Literal[
    "FRESH",
    "AGING",
    "STALE",
    "EXPIRED",
    "UNKNOWN",
]

PartnerStatusLiteral = Literal[
    "ACTIVE",
    "SUSPENDED",
    "REVOKED",
    "PROBATION",
]

AttributionStatusLiteral = Literal[
    "ATTRIBUTION_UNCONFIRMED",
    "SUSPECTED",
    "PLAUSIBLE",
    "HIGH_CONFIDENCE_ATTRIBUTED",
]


# ============================================================================
# Intelligence Object & Source Reliability
# ============================================================================

class IntelligenceSourceReliabilityDTO(BaseModel):
    """Source trust tracking record (Section 6-7). Tracked separately from confidence."""
    model_config = ConfigDict(from_attributes=True)

    source_id: str
    historical_accuracy: float = 0.85
    false_positive_rate: float = 0.05
    freshness_score: float = 0.90
    provenance_quality: float = 0.88
    validation_history_count: int = 1
    reliability_score: float = 0.85
    last_evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ThreatIntelligenceObjectDTO(BaseModel):
    """Canonical Threat Intelligence Object (Section 3-5)."""
    model_config = ConfigDict(from_attributes=True)

    intelligence_id: str = Field(default_factory=lambda: f"tio_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    source_type: str = "INTERNAL_OBSERVATION"
    source_id: str = "src_default"
    intelligence_type: IntelligenceTypeLiteral = "DOMAIN"
    canonical_identifier: str = ""
    raw_indicator: str = ""
    classification: DataClassificationLiteral = "INTERNAL"
    confidence: float = 0.75
    reliability: float = 0.85
    severity: Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"] = "MEDIUM"
    observed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None
    provenance: Dict[str, Any] = Field(default_factory=dict)
    validation_state: IntelligenceStateLiteral = "OBSERVED"
    sharing_state: SharingStateLiteral = "PRIVATE"
    content_hash: str = ""
    version: int = 1
    anonymized_tenant_cohort: Optional[str] = None
    contradictory_evidence: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    related_campaign_ids: List[str] = Field(default_factory=list)
    associated_modalities: List[str] = Field(default_factory=list)


# ============================================================================
# Privacy Transformation & Sharing Policy
# ============================================================================

class IntelligencePrivacyTransformationDTO(BaseModel):
    """Privacy Transformation record (Section 11-12)."""
    model_config = ConfigDict(from_attributes=True)

    transformation_id: str = Field(default_factory=lambda: f"pt_{uuid.uuid4().hex[:8]}")
    intelligence_id: str
    transformation_type: PrivacyTransformationTypeLiteral = "REDACT"
    detected_pii: List[str] = Field(default_factory=list)
    detected_secrets: List[str] = Field(default_factory=list)
    detected_customer_identifiers: List[str] = Field(default_factory=list)
    redacted_fields: List[str] = Field(default_factory=list)
    generalized_attributes: Dict[str, str] = Field(default_factory=dict)
    anonymized_cohort: str = "ANON_COHORT"
    is_safe_to_share: bool = False
    transformed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SharingPolicyEvaluationDTO(BaseModel):
    """Sharing Policy Evaluation Decision (Section 14-16)."""
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: str = Field(default_factory=lambda: f"spe_{uuid.uuid4().hex[:8]}")
    intelligence_id: str
    tenant_id: str
    decision: Literal["ALLOW", "DENY", "REDACT_AND_ALLOW", "AGGREGATE_ONLY"] = "DENY"
    reason: str = ""
    explicit_deny_triggered: bool = False
    consent_id: Optional[str] = None
    legal_jurisdiction: str = "GLOBAL"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Federation Protocol & Partner Registry
# ============================================================================

class FederationPartnerDTO(BaseModel):
    """Federation Partner Registry Record (Section 18-20)."""
    model_config = ConfigDict(from_attributes=True)

    partner_id: str = Field(default_factory=lambda: f"fp_{uuid.uuid4().hex[:8]}")
    name: str = "Partner Network"
    trust_level: float = 0.80
    supported_formats: List[str] = Field(default_factory=lambda: ["JSON", "STIX2.1", "TAXII2"])
    scopes: List[str] = Field(default_factory=lambda: ["threat_indicators", "campaign_summaries"])
    status: PartnerStatusLiteral = "ACTIVE"
    auth_key_hash: str = ""
    rate_limit_per_minute: int = 100
    current_minute_requests: int = 0
    total_received: int = 0
    total_rejected: int = 0
    last_sync: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class FederationBundleDTO(BaseModel):
    """Inbound or Outbound Signed Federation Intelligence Bundle (Section 17-21)."""
    model_config = ConfigDict(from_attributes=True)

    bundle_id: str = Field(default_factory=lambda: f"fbd_{uuid.uuid4().hex[:12]}")
    source_partner_id: str
    format: str = "JSON"
    signature: str = ""
    objects: List[ThreatIntelligenceObjectDTO] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Global Campaign Graph & Attribution Safety
# ============================================================================

class GlobalCampaignNodeDTO(BaseModel):
    """Node in Global Campaign Graph (Section 29-30)."""
    model_config = ConfigDict(from_attributes=True)

    node_id: str
    node_type: Literal["INDICATOR", "INFRASTRUCTURE", "CAMPAIGN", "ATTACK_PATTERN", "ANONYMIZED_COHORT"]
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.80
    is_verified: bool = False


class GlobalCampaignEdgeDTO(BaseModel):
    """Edge in Global Campaign Graph (Section 29-30)."""
    model_config = ConfigDict(from_attributes=True)

    edge_id: str = Field(default_factory=lambda: f"gce_{uuid.uuid4().hex[:8]}")
    source_node_id: str
    target_node_id: str
    relationship: Literal[
        "OBSERVED_WITH",
        "RELATED_TO",
        "REUSED_BY",
        "CORRELATED_WITH",
        "TEMPORALLY_RELATED",
        "INFRASTRUCTURE_REUSE",
        "CAMPAIGN_ASSOCIATION",
    ]
    confidence: float = 0.75
    supporting_evidence_count: int = 1
    contradictory_evidence_count: int = 0
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GlobalCampaignGraphDTO(BaseModel):
    """Global Campaign Graph Representation (Section 29)."""
    model_config = ConfigDict(from_attributes=True)

    nodes: List[GlobalCampaignNodeDTO] = Field(default_factory=list)
    edges: List[GlobalCampaignEdgeDTO] = Field(default_factory=list)
    total_campaigns: int = 0
    total_indicators: int = 0
    total_infrastructure_clusters: int = 0


class GlobalCampaignDetailDTO(BaseModel):
    """Detailed Campaign Summary Record (Section 31-35, 49)."""
    model_config = ConfigDict(from_attributes=True)

    campaign_id: str = Field(default_factory=lambda: f"gcmp_{uuid.uuid4().hex[:8]}")
    name: str = "Emerging Campaign"
    confidence: float = 0.70
    attribution_status: AttributionStatusLiteral = "ATTRIBUTION_UNCONFIRMED"
    attributed_actor: Optional[str] = None
    attribution_evidence: List[str] = Field(default_factory=list)
    indicators: List[str] = Field(default_factory=list)
    infrastructure_nodes: List[str] = Field(default_factory=list)
    modalities: List[str] = Field(default_factory=list)
    affected_cohorts: List[str] = Field(default_factory=list)
    expansion_velocity: float = 0.0  # indicators per hour
    expansion_warning: bool = False
    supporting_sources_count: int = 1
    contradictory_sources_count: int = 0
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Global Early Warning & Risk Signal
# ============================================================================

class GlobalEarlyWarningDTO(BaseModel):
    """Global Early Warning Broadcast (Section 36-37)."""
    model_config = ConfigDict(from_attributes=True)

    warning_id: str = Field(default_factory=lambda: f"gew_{uuid.uuid4().hex[:8]}")
    title: str
    summary: str
    confidence: float = 0.80
    trigger_type: Literal[
        "EMERGING_CAMPAIGN",
        "INFRASTRUCTURE_REUSE",
        "RAPID_EXPANSION",
        "MULTI_MODAL_EXPANSION",
        "ZERO_DAY_INDICATOR",
    ] = "EMERGING_CAMPAIGN"
    evidence_references: List[str] = Field(default_factory=list)
    scope: str = "GLOBAL"
    affected_sectors: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=lambda: ["Attribution unconfirmed; based on multi-source correlation"])
    recommended_threat_hunts: List[str] = Field(default_factory=list)
    issued_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GlobalThreatRiskSignalDTO(BaseModel):
    """Global Threat Risk Signal (Section 40)."""
    model_config = ConfigDict(from_attributes=True)

    signal_id: str = Field(default_factory=lambda: f"gtrs_{uuid.uuid4().hex[:8]}")
    threat_category: str
    risk_level: Literal["LOW", "ELEVATED", "HIGH", "SEVERE"] = "ELEVATED"
    confidence: float = 0.85
    expected_trend: Literal["ACCELERATING", "STABLE", "DECELERATING"] = "ACCELERATING"
    affected_sectors: List[str] = Field(default_factory=list)
    evidence_summary: str = ""
    is_confirmed_tenant_attack: bool = False  # Critical guardrail
    broadcast_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ThreatTrendReportDTO(BaseModel):
    """Threat Trend Report (Section 38, 54)."""
    model_config = ConfigDict(from_attributes=True)

    report_id: str = Field(default_factory=lambda: f"ttr_{uuid.uuid4().hex[:8]}")
    timeframe: str = "LAST_30_DAYS"
    indicator_growth_rate: float = 0.0
    campaign_growth_rate: float = 0.0
    top_modalities: List[Dict[str, Any]] = Field(default_factory=list)
    top_emerging_threats: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Tenant Relevance & Recommended Hunts
# ============================================================================

class TenantRelevanceDTO(BaseModel):
    """Tenant-Specific Threat Relevance Score & Personalized Feed (Section 41-43)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str
    intelligence_id: str
    overall_relevance_score: float = 0.0
    asset_overlap_score: float = 0.0
    industry_relevance_score: float = 0.0
    historical_exposure_score: float = 0.0
    recommended_hunts: List[str] = Field(default_factory=list)
    is_applicable: bool = False
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Dispute Management & Revocation Impact
# ============================================================================

class IntelligenceDisputeDTO(BaseModel):
    """Intelligence Dispute Record (Section 44-45)."""
    model_config = ConfigDict(from_attributes=True)

    dispute_id: str = Field(default_factory=lambda: f"dsp_{uuid.uuid4().hex[:8]}")
    intelligence_id: str
    submitter_tenant_id: str
    dispute_type: Literal["FALSE_POSITIVE", "OUTDATED", "IRRELEVANT", "FACTUALLY_INCORRECT", "BENIGN_SERVICE"] = "FALSE_POSITIVE"
    reason: str = ""
    evidence_submission: str = ""
    status: DisputeStatusLiteral = "OPEN"
    reviewer_notes: Optional[str] = None
    resolution: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: Optional[str] = None


class RevocationImpactAssessmentDTO(BaseModel):
    """Downstream Impact Analysis on Revocation (Section 27-28, 71)."""
    model_config = ConfigDict(from_attributes=True)

    revocation_id: str = Field(default_factory=lambda: f"rvk_{uuid.uuid4().hex[:8]}")
    intelligence_id: str
    reason: str
    revoked_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    revoked_by: str = "SYSTEM"
    affected_alerts_count: int = 0
    affected_incidents_count: int = 0
    affected_hunts_count: int = 0
    affected_predictions_count: int = 0
    affected_campaigns_count: int = 0
    affected_reports_count: int = 0
    reassessment_required: bool = True
    historical_provenance_preserved: bool = True


# ============================================================================
# Quality Score & Mission Control Center Summary
# ============================================================================

class IntelligenceQualityScoreDTO(BaseModel):
    """Multi-Dimensional Quality Score (Section 46)."""
    model_config = ConfigDict(from_attributes=True)

    intelligence_id: str
    freshness_status: FreshnessStatusLiteral = "FRESH"
    freshness_score: float = 1.0
    provenance_score: float = 1.0
    corroboration_score: float = 1.0
    source_reliability_score: float = 1.0
    validation_score: float = 1.0
    dispute_penalty: float = 0.0
    overall_quality_score: float = 1.0
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CollectiveDefenseCenterSummaryDTO(BaseModel):
    """Aggregated Collective Defense Center Summary (Section 50)."""
    model_config = ConfigDict(from_attributes=True)

    total_intelligence_objects: int = 0
    total_shared_objects: int = 0
    total_global_campaigns: int = 0
    active_early_warnings: int = 0
    active_federation_partners: int = 0
    open_disputes: int = 0
    revoked_indicators_count: int = 0
    average_quality_score: float = 0.0
    poisoning_alerts_count: int = 0
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
