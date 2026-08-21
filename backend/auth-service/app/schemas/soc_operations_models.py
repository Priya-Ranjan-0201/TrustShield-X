"""Pydantic v2 DTO Schemas for SOC Intelligence, Alert Correlation, Incident Response & SOAR Foundation (Phase 4.0 Part 7)."""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Sections 3-5, 9, 13-16, 23, 26, 31, 34, 43, 53)
# ============================================================================

AlertSourceLiteral = Literal[
    "INTERNAL_DETECTOR",
    "THREAT_INTELLIGENCE",
    "MONITORING",
    "GRAPH_CORRELATION",
    "ANALYST",
    "EXTERNAL_INTEGRATION",
    "AUTOMATED_RULE",
    "MODEL_ASSISTED",
]

AlertCategoryLiteral = Literal[
    "MALWARE",
    "PHISHING",
    "FINANCIAL_FRAUD",
    "IDENTITY_FRAUD",
    "VOICE_SCAM",
    "DEEPFAKE",
    "DOCUMENT_FRAUD",
    "QR_FRAUD",
    "ACCOUNT_COMPROMISE",
    "DATA_EXFILTRATION",
    "NETWORK_THREAT",
    "CAMPAIGN",
    "INFRASTRUCTURE",
    "OTHER",
]

ClusterTypeLiteral = Literal[
    "SAME_ENTITY",
    "SAME_CAMPAIGN",
    "SAME_ATTACK_CHAIN",
    "SAME_INFRASTRUCTURE",
    "SAME_INCIDENT",
    "TEMPORALLY_RELATED",
    "CROSS_MODAL",
    "POSSIBLE_RELATIONSHIP",
]

IncidentTypeLiteral = Literal[
    "MALWARE_INCIDENT",
    "PHISHING_INCIDENT",
    "FINANCIAL_FRAUD_INCIDENT",
    "IDENTITY_FRAUD_INCIDENT",
    "VOICE_SCAM_INCIDENT",
    "DEEPFAKE_INCIDENT",
    "DOCUMENT_FRAUD_INCIDENT",
    "QR_FRAUD_INCIDENT",
    "ACCOUNT_COMPROMISE",
    "DATA_EXFILTRATION",
    "MULTI_MODAL_INCIDENT",
    "UNKNOWN_INCIDENT",
]

IncidentStatusLiteral = Literal[
    "NEW",
    "TRIAGE",
    "ASSIGNED",
    "INVESTIGATING",
    "CONTAINMENT_PENDING",
    "CONTAINED",
    "ERADICATION",
    "RECOVERY",
    "RESOLVED",
    "CLOSED",
    "REOPENED",
    "CANCELLED",
]

IncidentSeverityLiteral = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFORMATIONAL",
]

IncidentPriorityLiteral = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFORMATIONAL",
]

ActionTypeLiteral = Literal[
    "BLOCK_DOMAIN",
    "BLOCK_IP",
    "BLOCK_URL",
    "QUARANTINE_FILE",
    "ISOLATE_DEVICE",
    "DISABLE_ACCOUNT",
    "REVOKE_TOKEN",
    "REVOKE_SESSION",
    "RESET_CREDENTIAL",
    "DISABLE_APPLICATION",
    "COLLECT_EVIDENCE",
    "CREATE_CASE",
    "NOTIFY_ANALYST",
    "NOTIFY_USER",
    "REQUEST_USER_CONFIRMATION",
    "ADD_IOC",
    "UPDATE_FIREWALL_RULE",
    "ADD_WAF_RULE",
    "MARK_INDICATOR",
    "FREEZE_UPI_HANDLE",
    "BLOCK_TRANSACTION",
    "ISOLATE_S3_BUCKET",
    "BLOCK_PUBLIC_ACCESS",
    "DELETE_RESOURCE",
    "REVOKE_INFRASTRUCTURE",
    "TERMINATE_ALL_SESSIONS",
    "PERMANENT_DELETE_DATA",
    "HARD_PURGE_RECORDS",
    "REVOKE_ROOT_CERTIFICATE",
    "NO_ACTION",
]

ApprovalStatusLiteral = Literal[
    "NOT_REQUIRED",
    "PENDING",
    "APPROVED",
    "REJECTED",
    "EXPIRED",
    "CANCELLED",
]

ExecutionStatusLiteral = Literal[
    "QUEUED",
    "VALIDATING",
    "WAITING_APPROVAL",
    "DRY_RUN",
    "EXECUTING",
    "VERIFYING",
    "COMPLETED",
    "FAILED",
    "ROLLBACK_PENDING",
    "ROLLING_BACK",
    "ROLLED_BACK",
    "CANCELLED",
    "TIMED_OUT",
    "UNKNOWN_EXECUTION_STATE",
]

SLAStatusLiteral = Literal[
    "ON_TRACK",
    "WARNING",
    "BREACHED",
    "PAUSED",
    "RESOLVED",
]

AutomationLevelLiteral = Literal[
    "MANUAL_ONLY",
    "ASSISTED",
    "APPROVAL_REQUIRED",
    "AUTOMATIC_ALLOWED",
    "AUTOMATIC_RESTRICTED",
]

TimelineEventTypeLiteral = Literal[
    "ALERT_CREATED",
    "ALERT_CORRELATED",
    "INCIDENT_CREATED",
    "TRIAGE_COMPLETED",
    "ANALYST_ASSIGNED",
    "EVIDENCE_ADDED",
    "INTELLIGENCE_UPDATED",
    "CAMPAIGN_LINKED",
    "ATTACK_CHAIN_UPDATED",
    "PLAYBOOK_SELECTED",
    "APPROVAL_REQUESTED",
    "APPROVED",
    "REJECTED",
    "SIMULATION_STARTED",
    "ACTION_STARTED",
    "ACTION_COMPLETED",
    "ACTION_FAILED",
    "VERIFICATION_COMPLETED",
    "ROLLBACK_STARTED",
    "ROLLBACK_COMPLETED",
    "INCIDENT_RESOLVED",
    "INCIDENT_CLOSED",
]


# ============================================================================
# Core SOC DTOs
# ============================================================================

class SOCAlertDTO(BaseModel):
    """Canonical normalized SOC Alert (Section 3)."""
    model_config = ConfigDict(from_attributes=True)

    alert_id: str = Field(default_factory=lambda: f"soc_alt_{uuid.uuid4().hex[:12]}")
    source_alert_id: Optional[str] = None
    source_system: AlertSourceLiteral = "INTERNAL_DETECTOR"
    alert_type: str = "SECURITY_ALERT"
    category: AlertCategoryLiteral = "OTHER"
    subcategory: Optional[str] = None
    title: str = "Security Alert"
    description: str = ""
    severity: IncidentSeverityLiteral = "MEDIUM"
    priority: IncidentPriorityLiteral = "MEDIUM"
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW, PROBABILISTIC
    status: str = "NEW"
    entity_ids: List[str] = Field(default_factory=list)
    finding_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    relationship_ids: List[str] = Field(default_factory=list)
    campaign_id: Optional[str] = None
    attack_chain_id: Optional[str] = None
    case_id: Optional[str] = None
    incident_id: Optional[str] = None
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    organization_id: Optional[str] = None
    raw_payload: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AlertClusterDTO(BaseModel):
    """Correlated cluster of security alerts (Section 8)."""
    model_config = ConfigDict(from_attributes=True)

    cluster_id: str = Field(default_factory=lambda: f"clst_{uuid.uuid4().hex[:12]}")
    alert_ids: List[str] = Field(default_factory=list)
    entity_ids: List[str] = Field(default_factory=list)
    campaign_id: Optional[str] = None
    confidence: float = 1.0
    cluster_type: ClusterTypeLiteral = "SAME_ENTITY"
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "ACTIVE"
    organization_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityIncidentDTO(BaseModel):
    """Enterprise SOC Security Incident record (Section 12)."""
    model_config = ConfigDict(from_attributes=True)

    incident_id: str = Field(default_factory=lambda: f"inc_{uuid.uuid4().hex[:12]}")
    incident_number: str = Field(default_factory=lambda: f"INC-{uuid.uuid4().hex[:6].upper()}")
    title: str = "Security Incident"
    description: str = ""

    incident_type: IncidentTypeLiteral = "UNKNOWN_INCIDENT"
    severity: IncidentSeverityLiteral = "MEDIUM"
    priority: IncidentPriorityLiteral = "MEDIUM"
    confidence: str = "HIGH"
    status: IncidentStatusLiteral = "NEW"
    owner_id: Optional[str] = None
    team_id: Optional[str] = None
    source_alert_count: int = 0
    entity_count: int = 0
    finding_count: int = 0
    evidence_count: int = 0
    campaign_id: Optional[str] = None
    attack_chain_id: Optional[str] = None
    case_id: Optional[str] = None
    incident_fingerprint: str = ""
    organization_id: Optional[str] = None
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    acknowledged_at: Optional[str] = None
    contained_at: Optional[str] = None
    resolved_at: Optional[str] = None
    closed_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TriageResultDTO(BaseModel):
    """Automated Triage assessment result (Section 18)."""
    model_config = ConfigDict(from_attributes=True)

    triage_id: str = Field(default_factory=lambda: f"trg_{uuid.uuid4().hex[:12]}")
    incident_id: str
    classification: str
    severity: IncidentSeverityLiteral
    priority: IncidentPriorityLiteral
    confidence: str
    summary: str
    affected_entities: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    finding_ids: List[str] = Field(default_factory=list)
    recommended_actions: List[Dict[str, Any]] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IncidentTimelineEventDTO(BaseModel):
    """Auditable chronological incident event (Section 22)."""
    model_config = ConfigDict(from_attributes=True)

    timeline_event_id: str = Field(default_factory=lambda: f"tle_{uuid.uuid4().hex[:12]}")
    incident_id: str
    event_type: TimelineEventTypeLiteral
    source: str = "SOC_AUTOMATION"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actor: str = "SYSTEM"
    description: str
    entity_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    alert_id: Optional[str] = None
    action_id: Optional[str] = None
    provenance: str = ""


class IncidentAssignmentDTO(BaseModel):
    """Incident analyst assignment record (Section 24)."""
    model_config = ConfigDict(from_attributes=True)

    assignment_id: str = Field(default_factory=lambda: f"asgn_{uuid.uuid4().hex[:12]}")
    incident_id: str
    analyst_id: str
    team_id: Optional[str] = None
    assigned_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    assigned_by: str = "SOC_LEAD"
    reason: str = "Automated routing"
    status: str = "ACTIVE"


class IncidentSLADTO(BaseModel):
    """Incident SLA deadline and breach tracker (Section 25)."""
    model_config = ConfigDict(from_attributes=True)

    sla_id: str = Field(default_factory=lambda: f"sla_{uuid.uuid4().hex[:12]}")
    incident_id: str
    ack_deadline: str
    triage_deadline: str
    containment_deadline: str
    resolution_deadline: str
    status: SLAStatusLiteral = "ON_TRACK"
    time_to_acknowledge_seconds: Optional[float] = None
    time_to_triage_seconds: Optional[float] = None
    time_to_containment_seconds: Optional[float] = None
    time_to_resolution_seconds: Optional[float] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Playbook & Response SOAR DTOs (Sections 28, 30, 33, 35, 46, 47, 52)
# ============================================================================

class PlaybookStepDTO(BaseModel):
    """Individual executable step within a response playbook (Section 30)."""
    model_config = ConfigDict(from_attributes=True)

    step_id: str = Field(default_factory=lambda: f"step_{uuid.uuid4().hex[:12]}")
    playbook_id: str
    step_number: int
    name: str
    description: str
    action_type: ActionTypeLiteral
    risk_level: IncidentSeverityLiteral = "MEDIUM"
    approval_required: bool = True
    dry_run_supported: bool = True
    rollback_supported: bool = False
    timeout: int = 30  # seconds
    retry_policy: Dict[str, Any] = Field(default_factory=lambda: {"max_retries": 0, "backoff": 2.0})
    conditions: Dict[str, Any] = Field(default_factory=dict)


class ResponsePlaybookVersionDTO(BaseModel):
    """Immutable published version of a response playbook (Section 29, 85)."""
    model_config = ConfigDict(from_attributes=True)

    version_id: str = Field(default_factory=lambda: f"pbv_{uuid.uuid4().hex[:12]}")
    playbook_id: str
    version_number: int = 1
    content_hash: str = ""
    author: str = "SOC_ADMIN"
    steps: List[PlaybookStepDTO] = Field(default_factory=list)
    published_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResponsePlaybookDTO(BaseModel):
    """Controlled incident response workflow definition (Section 28)."""
    model_config = ConfigDict(from_attributes=True)

    playbook_id: str = Field(default_factory=lambda: f"pbk_{uuid.uuid4().hex[:12]}")
    name: str
    current_version: int = 1
    description: str
    incident_types: List[IncidentTypeLiteral] = Field(default_factory=list)
    required_permissions: List[str] = Field(default_factory=list)
    approval_policy: Dict[str, Any] = Field(default_factory=dict)
    steps: List[PlaybookStepDTO] = Field(default_factory=list)
    enabled: bool = True
    organization_id: Optional[str] = None
    created_by: str = "SOC_ADMIN"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResponseActionDTO(BaseModel):
    """Concrete remediation or containment action instance (Section 33)."""
    model_config = ConfigDict(from_attributes=True)

    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:12]}")
    incident_id: str
    playbook_id: Optional[str] = None
    playbook_version: int = 1
    step_id: Optional[str] = None
    action_type: ActionTypeLiteral
    target: str
    target_type: str = "DOMAIN"
    requested_by: str
    approved_by: Optional[str] = None
    approval_status: ApprovalStatusLiteral = "PENDING"
    dry_run: bool = False
    status: ExecutionStatusLiteral = "QUEUED"
    reason: str
    evidence_ids: List[str] = Field(default_factory=list)
    idempotency_key: str = Field(default_factory=lambda: f"idemp_{uuid.uuid4().hex}")
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_code: Optional[str] = None
    result_reference: Optional[str] = None
    rollback_action_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ApprovalRequestDTO(BaseModel):
    """Four-eyes authorization request for high-impact action (Section 35, 80)."""
    model_config = ConfigDict(from_attributes=True)

    approval_id: str = Field(default_factory=lambda: f"appr_{uuid.uuid4().hex[:12]}")
    action_id: str
    incident_id: str
    requested_by: str
    approver_scope: str = "SOC_LEAD"
    reason: str
    risk: IncidentSeverityLiteral = "HIGH"
    evidence: List[str] = Field(default_factory=list)
    expires_at: str
    status: ApprovalStatusLiteral = "PENDING"
    decision_reason: Optional[str] = None
    decided_by: Optional[str] = None
    decided_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResponseSimulationDTO(BaseModel):
    """Dry-run simulation execution artifact (Section 38)."""
    model_config = ConfigDict(from_attributes=True)

    simulation_id: str = Field(default_factory=lambda: f"sim_{uuid.uuid4().hex[:12]}")
    action_id: str
    target: str
    provider: str
    expected_effect: str
    risk_assessment: str
    required_permissions: List[str] = Field(default_factory=list)
    rollback_supported: bool
    side_effects: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResponseExecutionDTO(BaseModel):
    """Record of actual provider execution (Section 39)."""
    model_config = ConfigDict(from_attributes=True)

    execution_id: str = Field(default_factory=lambda: f"exec_{uuid.uuid4().hex[:12]}")
    action_id: str
    provider_name: str
    status: ExecutionStatusLiteral
    request_payload: Dict[str, Any] = Field(default_factory=dict)
    response_payload: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResponseVerificationDTO(BaseModel):
    """Empirical verification record of containment or remediation (Section 47)."""
    model_config = ConfigDict(from_attributes=True)

    verification_id: str = Field(default_factory=lambda: f"ver_{uuid.uuid4().hex[:12]}")
    action_id: str
    target: str
    verification_status: Literal["SUCCESS", "PARTIAL", "FAILED", "UNKNOWN"]
    evidence_gathered: List[str] = Field(default_factory=list)
    observations: str
    verified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResponseRollbackDTO(BaseModel):
    """Rollback execution record (Section 46)."""
    model_config = ConfigDict(from_attributes=True)

    rollback_id: str = Field(default_factory=lambda: f"rol_{uuid.uuid4().hex[:12]}")
    action_id: str
    target: str
    rollback_status: Literal["ROLLED_BACK", "ROLLBACK_FAILED", "ROLLBACK_UNAVAILABLE"]
    reason: str
    executed_by: str
    error_message: Optional[str] = None
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EvidenceCollectionRecordDTO(BaseModel):
    """Chain-of-custody tracking record for collected digital evidence (Sections 63-65)."""
    model_config = ConfigDict(from_attributes=True)

    collection_id: str = Field(default_factory=lambda: f"evc_{uuid.uuid4().hex[:12]}")
    incident_id: str
    source: str
    collector_id: str
    evidence_type: str
    sha256_hash: str
    storage_reference: str
    integrity_status: str = "VERIFIED"
    collection_method: str = "SECURE_API_PULL"
    access_log: List[Dict[str, Any]] = Field(default_factory=list)
    collected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IncidentMergeRecordDTO(BaseModel):
    """Record of two incidents merged into one (Section 60)."""
    model_config = ConfigDict(from_attributes=True)

    merge_id: str = Field(default_factory=lambda: f"mrg_{uuid.uuid4().hex[:12]}")
    primary_incident_id: str
    merged_incident_ids: List[str] = Field(default_factory=list)
    merged_by: str
    reason: str
    status: Literal["MERGE_CANDIDATE", "MERGE_APPROVED", "MERGED", "REJECTED"] = "MERGED"
    merged_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IncidentSplitRecordDTO(BaseModel):
    """Record of an incident split into separate entities (Section 61)."""
    model_config = ConfigDict(from_attributes=True)

    split_id: str = Field(default_factory=lambda: f"splt_{uuid.uuid4().hex[:12]}")
    original_incident_id: str
    new_incident_ids: List[str] = Field(default_factory=list)
    split_by: str
    reason: str
    split_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
