"""
TruthShield X — Phase 9 Digital Threat Fusion & Security Operations Fabric Data Models
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


SecurityEventTypeLiteral = Literal[
    "OBSERVATION",
    "DETECTION",
    "THREAT_SIGNAL",
    "ASSET_CHANGE",
    "EXPOSURE_CHANGE",
    "TRUST_CHANGE",
    "RISK_CHANGE",
    "CAMPAIGN_UPDATE",
    "PREDICTION",
    "ALERT",
    "INCIDENT_UPDATE",
    "RESPONSE_ACTION",
    "RESPONSE_RESULT",
    "VERIFICATION_RESULT",
    "AUDIT_EVENT",
]

CampaignStateLiteral = Literal[
    "EMERGING",
    "ACTIVE",
    "ESCALATING",
    "CONTAINMENT",
    "CONTAINED",
    "DORMANT",
    "REACTIVATED",
    "RESOLVED",
    "ARCHIVED",
]

IncidentObjectiveLiteral = Literal[
    "IDENTIFY",
    "CONTAIN",
    "ERADICATE",
    "RECOVER",
    "VERIFY",
    "MONITOR",
]

PostureTrendLiteral = Literal[
    "improving",
    "stable",
    "degrading",
    "rapidly_degrading",
    "unknown",
]


class SecurityEventDTO(BaseModel):
    event_id: str
    event_type: SecurityEventTypeLiteral
    tenant_id: str = "default_tenant"
    source: str
    source_event_id: Optional[str] = None
    asset_id: Optional[str] = None
    entity_id: Optional[str] = None
    campaign_id: Optional[str] = None
    incident_id: Optional[str] = None
    severity: str = "MEDIUM"
    confidence: float = 0.90
    risk_score: float = 20.0
    trust_score: float = 80.0
    exposure_score: float = 20.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    observed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ingested_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provenance: Dict[str, Any] = Field(default_factory=dict)
    classification: str = "INTERNAL"
    status: str = "PROCESSED"
    correlation_id: Optional[str] = None
    content_fingerprint: Optional[str] = None


class EventCorrelationResultDTO(BaseModel):
    correlation_id: str
    correlation_type: str
    confidence: float
    supporting_event_ids: List[str] = Field(default_factory=list)
    counter_event_ids: List[str] = Field(default_factory=list)
    reason: str
    tenant_id: str = "default_tenant"
    correlated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ThreatFusionScoreDTO(BaseModel):
    fusion_score: float
    confidence: float
    converged_modalities: List[str]
    supporting_signals_count: int
    counter_signals_count: int
    explanation: str
    methodology: str = "Bayesian Multi-Modal Evidence Convergence (Weighted by Source Reliability & Temporal Proximity)"
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ThreatClusterDTO(BaseModel):
    cluster_id: str
    cluster_type: str  # CAMPAIGN, INCIDENT, MULTI_MODAL_ATTACK, PHISHING, PAYMENT_FRAUD, MALWARE
    tenant_id: str = "default_tenant"
    title: str
    summary: str
    event_ids: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    assets: List[str] = Field(default_factory=list)
    modalities: List[str] = Field(default_factory=list)
    fusion_score: float
    severity: str = "HIGH"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecuritySituationDTO(BaseModel):
    situation_id: str
    tenant_id: str = "default_tenant"
    active_threats_count: int
    critical_assets_count: int
    high_risk_exposure_count: int
    active_campaigns_count: int
    open_incidents_count: int
    new_anomalies_count: int
    trust_degradation_events: int
    predictive_warnings_count: int
    pending_responses_count: int
    verification_failures_count: int
    overall_threat_level: str = "ELEVATED"
    summary: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityPostureDTO(BaseModel):
    posture_id: str
    tenant_id: str = "default_tenant"
    overall_posture_score: float  # 0 - 100 (Higher is healthier/better protected)
    risk_score: float             # Danger
    trust_score: float            # Reliability
    exposure_score: float         # Attack surface
    trend: PostureTrendLiteral = "stable"
    trend_explanation: str
    dimensions: Dict[str, float] = Field(default_factory=dict)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BlastRadiusDTO(BaseModel):
    target_entity_or_asset: str
    blast_radius_score: float
    affected_assets: List[str] = Field(default_factory=list)
    connected_entities: List[str] = Field(default_factory=list)
    related_campaigns: List[str] = Field(default_factory=list)
    affected_services: List[str] = Field(default_factory=list)
    affected_identities: List[str] = Field(default_factory=list)
    impact_level: str = "POTENTIAL_IMPACT"
    rationale: str


class AttackPathNodeDTO(BaseModel):
    node_id: str
    node_type: str  # ENTRY, COMPROMISED_ENTITY, INFRASTRUCTURE, CAMPAIGN, TARGET
    label: str
    status: str     # OBSERVED_PATH, POTENTIAL_PATH, INFERRED_PATH
    confidence: float


class AttackPathDTO(BaseModel):
    path_id: str
    target_asset: str
    path_nodes: List[AttackPathNodeDTO]
    overall_confidence: float
    constructed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityNarrativeDTO(BaseModel):
    narrative_id: str
    target_subject: str
    what_happened: str
    when_observed: str
    what_was_observed: str
    what_is_verified: str
    what_is_correlated: str
    what_is_inferred: str
    current_risk: float
    current_trust: float
    current_exposure: float
    potential_impact: str
    actions_taken: List[str] = Field(default_factory=list)
    verified_post_response: str
    what_remains_unknown: str
    recommended_next_step: str
    citations: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IncidentObjectiveDTO(BaseModel):
    objective_id: str
    objective_type: IncidentObjectiveLiteral
    owner: str
    status: str = "IN_PROGRESS"  # PENDING, IN_PROGRESS, COMPLETED, BLOCKED
    evidence_ids: List[str] = Field(default_factory=list)
    deadline: Optional[str] = None
    completion_criteria: str


class IncidentChecklistItemDTO(BaseModel):
    item_id: str
    task_description: str
    is_completed: bool = False
    evidence_id: Optional[str] = None
    verified_by: Optional[str] = None


class IncidentCommandStateDTO(BaseModel):
    incident_id: str
    tenant_id: str = "default_tenant"
    commander: str
    severity: str
    status: str
    affected_assets: List[str] = Field(default_factory=list)
    campaign_id: Optional[str] = None
    current_objective: IncidentObjectiveLiteral = "IDENTIFY"
    objectives: List[IncidentObjectiveDTO] = Field(default_factory=list)
    checklist: List[IncidentChecklistItemDTO] = Field(default_factory=list)
    containment_status: str = "NOT_CONTAINED"
    response_status: str = "RECOMMENDED"
    verification_status: str = "PENDING"
    next_action: str
    open_questions: List[str] = Field(default_factory=list)
    last_updated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityKpisDTO(BaseModel):
    tenant_id: str = "default_tenant"
    mttd_minutes: float  # Mean Time to Detect
    mtti_minutes: float  # Mean Time to Investigate
    mttc_minutes: float  # Mean Time to Contain
    mttr_minutes: float  # Mean Time to Recover
    mttv_minutes: float  # Mean Time to Verify
    active_incidents: int
    critical_alerts: int
    false_positive_rate: float
    response_success_rate: float
    verification_failure_rate: float
    prediction_accuracy: float
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SubsystemHealthDTO(BaseModel):
    subsystem_name: str
    status: str  # HEALTHY, DEGRADED, SERVICE_DEGRADED, UNAVAILABLE
    impact: str
    last_successful_operation: str
    recovery_status: str


class SecurityHealthOverviewDTO(BaseModel):
    overall_health: str  # HEALTHY, DEGRADED, UNHEALTHY
    subsystems: Dict[str, SubsystemHealthDTO]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DataQualityFindingDTO(BaseModel):
    finding_id: str
    quality_issue: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    affected_record_id: str
    details: str
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
