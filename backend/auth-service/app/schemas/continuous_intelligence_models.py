"""Pydantic v2 DTO Schemas for Real-Time Trust Monitoring & Continuous Intelligence (Phase 4.0 Part 6)."""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timezone


# ============================================================================
# Enums and Taxonomy Literals
# ============================================================================

ProviderTypeLiteral = Literal[
    "STIX_TAXII",
    "CSV_FEED",
    "JSON_FEED",
    "REST_API",
    "LOCAL_DATABASE",
    "COMMERCIAL_FEED",
    "OPEN_SOURCE_FEED",
    "INTERNAL_ANALYST_FEED",
]

FeedHealthStatusLiteral = Literal[
    "HEALTHY",
    "DEGRADED",
    "STALE",
    "UNAVAILABLE",
    "AUTH_FAILURE",
    "RATE_LIMITED",
    "INVALID_DATA",
    "DISABLED",
    "UNKNOWN",
]

ObservationTypeLiteral = Literal[
    "NEW",
    "UPDATED",
    "REVOKED",
    "EXPIRED",
    "RECLASSIFIED",
    "CONFIRMED",
    "DISPUTED",
    "REMOVED",
    "REACTIVATED",
]

IOCLifecycleLiteral = Literal[
    "DISCOVERED",
    "ACTIVE",
    "STALE",
    "EXPIRED",
    "REVOKED",
    "DISPUTED",
    "ARCHIVED",
]

IOCTypeLiteral = Literal[
    "IPv4",
    "IPv6",
    "DOMAIN",
    "URL",
    "EMAIL",
    "HASH",
    "FILE",
    "CERTIFICATE",
    "PACKAGE",
    "PHONE",
    "UPI",
    "ACCOUNT",
    "MALWARE_FAMILY",
    "PHISHING_KIT",
]

FeedTrustLevelLiteral = Literal[
    "AUTHORITATIVE",
    "TRUSTED",
    "STANDARD",
    "LOW_TRUST",
    "UNVERIFIED",
]

FreshnessStatusLiteral = Literal[
    "HOT",
    "CURRENT",
    "AGING",
    "STALE",
    "EXPIRED",
    "UNKNOWN",
]

IntelligenceEventTypeLiteral = Literal[
    "IOC_NEW",
    "IOC_UPDATED",
    "IOC_REVOKED",
    "IOC_EXPIRED",
    "IOC_RECLASSIFIED",
    "THREAT_MATCH_NEW",
    "THREAT_MATCH_REMOVED",
    "DOMAIN_CHANGED",
    "CERTIFICATE_CHANGED",
    "INFRASTRUCTURE_CHANGED",
    "CAMPAIGN_CHANGED",
    "RELATIONSHIP_CHANGED",
    "FEED_STATUS_CHANGED",
    "ANALYSIS_REASSESSMENT_REQUIRED",
]

ImpactLevelLiteral = Literal[
    "NO_IMPACT",
    "LOW_IMPACT",
    "MEDIUM_IMPACT",
    "HIGH_IMPACT",
    "CRITICAL_IMPACT",
]

AlertPriorityLiteral = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFORMATIONAL",
]

AlertSeverityLiteral = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFORMATIONAL",
]

AlertStatusLiteral = Literal[
    "NEW",
    "ACKNOWLEDGED",
    "IN_PROGRESS",
    "ESCALATED",
    "SUPPRESSED",
    "RESOLVED",
    "CLOSED",
    "REOPENED",
    "EXPIRED",
]

AlertTypeLiteral = Literal[
    "NEW_THREAT_MATCH",
    "THREAT_RECLASSIFICATION",
    "MALICIOUS_DOMAIN",
    "MALICIOUS_IP",
    "MALICIOUS_HASH",
    "CAMPAIGN_UPDATE",
    "ATTACK_CHAIN_UPDATE",
    "CERTIFICATE_CHANGE",
    "INFRASTRUCTURE_CHANGE",
    "HIGH_IMPACT_CORRELATION",
    "FEED_FAILURE",
    "FEED_STALE",
    "REASSESSMENT_REQUIRED",
]

NotificationChannelLiteral = Literal[
    "IN_APP",
    "EMAIL",
    "PUSH",
    "WEBHOOK",
    "SMS",
    "SLACK",
    "TEAMS",
]

NotificationStatusLiteral = Literal[
    "QUEUED",
    "SENDING",
    "SENT",
    "DELIVERED",
    "FAILED",
    "RETRYING",
    "CANCELLED",
    "UNKNOWN",
]

IncidentTypeLiteral = Literal[
    "PHISHING_INCIDENT",
    "MALWARE_INCIDENT",
    "FINANCIAL_FRAUD_INCIDENT",
    "IDENTITY_FRAUD_INCIDENT",
    "VOICE_SCAM_INCIDENT",
    "QR_FRAUD_INCIDENT",
    "DOCUMENT_FRAUD_INCIDENT",
    "MULTI_MODAL_INCIDENT",
    "UNKNOWN_INCIDENT",
]

IncidentStatusLiteral = Literal[
    "DETECTED",
    "TRIAGED",
    "INVESTIGATING",
    "CONTAINED",
    "ERADICATED",
    "RECOVERED",
    "CLOSED",
    "REOPENED",
]


# ============================================================================
# Feed Configuration & Health DTOs
# ============================================================================

class ThreatFeedConfigurationDTO(BaseModel):
    feed_id: str
    provider_name: str
    provider_type: ProviderTypeLiteral
    endpoint: str
    enabled: bool = True
    poll_interval: str = "HOURLY"
    poll_interval_seconds: int = 3600
    authentication_mode: str = "NONE"
    timeout_seconds: int = 30
    retry_policy: Dict[str, Any] = Field(default_factory=lambda: {"max_retries": 3, "backoff_factor": 2.0})
    rate_limit: Dict[str, Any] = Field(default_factory=lambda: {"max_requests_per_minute": 60})
    supported_types: List[str] = Field(default_factory=list)
    trust_level: FeedTrustLevelLiteral = "STANDARD"
    freshness_policy: Dict[str, Any] = Field(default_factory=lambda: {"stale_after_days": 30, "expire_after_days": 90})
    organization_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ThreatFeedHealthDTO(BaseModel):
    health_id: str
    feed_id: str
    status: FeedHealthStatusLiteral = "UNKNOWN"
    last_success: Optional[str] = None
    last_failure: Optional[str] = None
    last_attempt: Optional[str] = None
    latency_ms: float = 0.0
    items_received: int = 0
    items_accepted: int = 0
    items_rejected: int = 0
    parse_errors: int = 0
    authentication_errors: int = 0
    rate_limit_errors: int = 0
    network_errors: int = 0
    staleness_days: float = 0.0
    provider_version: str = "1.0.0"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ThreatFeedVersionDTO(BaseModel):
    version_id: str
    feed_id: str
    version_tag: str
    content_hash: str
    items_count: int
    fetched_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Intelligence Observation & Lifecycle DTOs
# ============================================================================

class IntelligenceObservationDTO(BaseModel):
    observation_id: str
    feed_id: str
    indicator_id: str
    indicator_type: str
    indicator_value_hash: str
    normalized_value: str
    raw_value: str
    observation_type: ObservationTypeLiteral = "NEW"
    classification: str = "MALICIOUS"
    confidence: str = "HIGH"
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    observed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_timestamp: Optional[str] = None
    feed_version: str = "1.0.0"
    raw_reference: Optional[str] = None
    status: IOCLifecycleLiteral = "ACTIVE"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceStateChangeDTO(BaseModel):
    change_id: str
    entity_id: str
    observation_id: str
    previous_state: str
    new_state: str
    transition_reason: str
    transition_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str


# ============================================================================
# Monitoring Jobs DTOs
# ============================================================================

class MonitoringJobDTO(BaseModel):
    job_id: str
    feed_id: str
    job_type: str = "SYNC"
    schedule_type: str = "HOURLY"
    interval_seconds: int = 3600
    cron_expression: Optional[str] = None
    enabled: bool = True
    next_run_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_run_at: Optional[str] = None
    status: str = "QUEUED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MonitoringJobRunDTO(BaseModel):
    run_id: str
    job_id: str
    feed_id: str
    status: str = "RUNNING"
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    attempt: int = 1
    items_processed: int = 0
    items_failed: int = 0
    error_code: Optional[str] = None
    error_message: Optional[str] = None


# ============================================================================
# Intelligence Events & Dead Letter Queue DTOs
# ============================================================================

class IntelligenceChangeEventDTO(BaseModel):
    event_id: str
    event_type: IntelligenceEventTypeLiteral
    entity_id: str
    analysis_id: Optional[str] = None
    case_id: Optional[str] = None
    previous_state: str
    new_state: str
    source: str
    confidence: str = "HIGH"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    feed_version: str = "1.0.0"
    provenance: str = ""
    severity: AlertSeverityLiteral = "HIGH"
    status: str = "ACTIVE"


class IntelligenceEventDTO(BaseModel):
    event_id: str
    event_type: IntelligenceEventTypeLiteral
    event_version: str = "1.0.0"
    schema_version: str = "1.0.0"
    producer: str = "continuous_intelligence_orchestrator"
    entity_id: Optional[str] = None
    analysis_id: Optional[str] = None
    case_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: str = ""
    causation_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    provenance: str = ""
    deduplication_key: str = ""


class EventProcessingRecordDTO(BaseModel):
    record_id: str
    event_id: str
    consumer_id: str
    status: str = "PROCESSED"
    attempts: int = 1
    processed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error_message: Optional[str] = None


class EventDeadLetterDTO(BaseModel):
    dead_letter_id: str
    event_id: str
    error: str
    attempts: int
    last_attempt: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    consumer: str
    payload_reference: str
    status: str = "PENDING"
    reprocessed_at: Optional[str] = None
    reprocessed_by: Optional[str] = None


# ============================================================================
# Security Alerts, Fingerprints, Suppression & Escalation DTOs
# ============================================================================

class SecurityAlertDTO(BaseModel):
    alert_id: str
    case_id: Optional[str] = None
    analysis_id: Optional[str] = None
    event_id: Optional[str] = None
    alert_type: AlertTypeLiteral
    title: str
    description: str
    priority: AlertPriorityLiteral = "MEDIUM"
    severity: AlertSeverityLiteral = "MEDIUM"
    confidence: str = "HIGH"
    status: AlertStatusLiteral = "NEW"
    source: str = "THREAT_MONITOR"
    evidence_ids: List[str] = Field(default_factory=list)
    finding_ids: List[str] = Field(default_factory=list)
    entity_ids: List[str] = Field(default_factory=list)
    relationship_ids: List[str] = Field(default_factory=list)
    campaign_id: Optional[str] = None
    attack_chain_id: Optional[str] = None
    alert_fingerprint: str = ""
    organization_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    acknowledged_at: Optional[str] = None
    resolved_at: Optional[str] = None
    suppressed_until: Optional[str] = None


class AlertFingerprintDTO(BaseModel):
    fingerprint_id: str
    fingerprint_hash: str
    alert_type: str
    entity_id: Optional[str] = None
    case_id: Optional[str] = None
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    occurrences: int = 1


class AlertSuppressionDTO(BaseModel):
    suppression_id: str
    alert_fingerprint: str
    alert_type: str
    reason: str
    suppressed_by: str
    expires_at: Optional[str] = None
    is_active: bool = True
    allow_critical_override: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AlertAcknowledgementDTO(BaseModel):
    ack_id: str
    alert_id: str
    user_id: str
    user_name: str
    reason: str
    comment: Optional[str] = None
    acknowledged_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AlertEscalationDTO(BaseModel):
    escalation_id: str
    alert_id: str
    previous_priority: AlertPriorityLiteral
    escalated_priority: AlertPriorityLiteral
    escalation_type: str = "TIMEOUT"
    reason: str
    escalated_by: Optional[str] = None
    escalated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Notifications DTOs
# ============================================================================

class NotificationPolicyDTO(BaseModel):
    policy_id: str
    organization_id: Optional[str] = None
    alert_type: str
    min_priority: AlertPriorityLiteral = "HIGH"
    channel: NotificationChannelLiteral = "IN_APP"
    enabled: bool = True
    cooldown_minutes: int = 15
    recipient_scope: str = "SOC_ANALYSTS"
    recipient_targets: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class NotificationDeliveryDTO(BaseModel):
    delivery_id: str
    alert_id: str
    policy_id: Optional[str] = None
    channel: NotificationChannelLiteral
    recipient: str
    delivery_status: NotificationStatusLiteral = "QUEUED"
    sent_at: Optional[str] = None
    delivered_at: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Reassessments & Risk Versioning DTOs
# ============================================================================

class IntelligenceReassessmentDTO(BaseModel):
    reassessment_id: str
    analysis_id: str
    case_id: Optional[str] = None
    trigger_event_id: str
    impact_level: ImpactLevelLiteral
    previous_risk_score: float
    proposed_risk_score: float
    status: str = "PENDING_APPROVAL"
    requested_by: str = "SYSTEM_AUTOMATION"
    approved_by: Optional[str] = None
    reason: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: Optional[str] = None


class RiskAssessmentVersionDTO(BaseModel):
    version_id: str
    analysis_id: str
    report_id: str
    version_number: int
    risk_score: float
    risk_band: str
    confidence: str
    policy_version: str = "1.0.0"
    trigger_event_id: Optional[str] = None
    supporting_intelligence: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Incidents, Report Updates & Realtime DTOs
# ============================================================================

class SecurityIncidentDTO(BaseModel):
    incident_id: str
    case_id: Optional[str] = None
    incident_type: IncidentTypeLiteral = "UNKNOWN_INCIDENT"
    title: str
    status: IncidentStatusLiteral = "DETECTED"
    priority: AlertPriorityLiteral = "MEDIUM"
    severity: AlertSeverityLiteral = "MEDIUM"
    confidence: str = "HIGH"
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    alert_count: int = 1
    entity_count: int = 1
    finding_count: int = 0
    campaign_id: Optional[str] = None
    attack_chain_id: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ReportUpdateEventDTO(BaseModel):
    update_event_id: str
    report_id: str
    previous_version: int
    new_version: int
    change_reason: str
    intelligence_source_ids: List[str] = Field(default_factory=list)
    triggered_by: str = "SYSTEM_REASSESSMENT"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RealtimeSubscriptionDTO(BaseModel):
    subscription_id: str
    client_id: str
    user_id: str
    organization_id: Optional[str] = None
    channel_scope: str = "ALL"
    case_ids: List[str] = Field(default_factory=list)
    analysis_ids: List[str] = Field(default_factory=list)
    subscribed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_heartbeat: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# API Request / Response DTOs
# ============================================================================

class ThreatFeedSyncRequestDTO(BaseModel):
    force: bool = False
    dry_run: bool = False


class ThreatFeedSyncResponseDTO(BaseModel):
    feed_id: str
    status: str
    items_received: int
    items_accepted: int
    items_rejected: int
    changes_detected: int
    events_published: int
    alerts_generated: int
    execution_time_ms: float


class AlertAcknowledgeRequestDTO(BaseModel):
    reason: str
    comment: Optional[str] = None


class AlertEscalateRequestDTO(BaseModel):
    priority: AlertPriorityLiteral
    reason: str


class AlertSuppressRequestDTO(BaseModel):
    reason: str
    duration_hours: Optional[int] = 24
    allow_critical_override: bool = True
