"""
TruthShield X — Autonomous SOC Orchestration & Closed-Loop Defense Models (Phase 21).

Strictly typed Pydantic models for Alert Normalization, Priority Scoring, False Positive Learning,
Incident State Machine, Blast Radius, Playbooks & Validation, Action Execution & Verifications,
Automation Guardrails, Emergency Stops, Case & Task Management, and SOC Scorecards.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 21)
# ============================================================================

SOCAlertSeverityLiteral = Literal[
    "INFORMATIONAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]

SOCIncidentStateLiteral = Literal[
    "NEW",
    "TRIAGED",
    "INVESTIGATING",
    "CONTAINMENT_PENDING",
    "CONTAINED",
    "ERADICATION",
    "RECOVERY",
    "VALIDATION",
    "CLOSED",
    "REOPENED",
    "ESCALATED",
    "CANCELLED",
]

SOCActionStateLiteral = Literal[
    "REQUESTED",
    "AUTHORIZATION_CHECKED",
    "APPROVAL_PENDING",
    "APPROVED",
    "EXECUTING",
    "EXECUTED",
    "VERIFYING",
    "VERIFIED",
    "PARTIAL",
    "FAILED",
    "ROLLED_BACK",
    "BLOCKED",
]

ActionVerificationStatusLiteral = Literal[
    "VERIFIED_SUCCESS",
    "PARTIAL_SUCCESS",
    "FAILED",
    "UNKNOWN",
]

PlaybookNodeTypeLiteral = Literal[
    "TRIGGER",
    "ENRICH",
    "CONDITION",
    "SIMULATE",
    "APPROVAL",
    "ACTION",
    "VERIFY",
    "WAIT",
    "ESCALATE",
    "NOTIFY",
    "RECOVER",
    "END",
]


# ============================================================================
# Alert Normalization, Deduplication & Priority DTOs
# ============================================================================

class SOCAlertNormalizedDTO(BaseModel):
    alert_id: str = Field(default_factory=lambda: f"alt_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    source: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    severity: SOCAlertSeverityLiteral = "HIGH"
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    evidence: List[str] = Field(default_factory=list)
    asset: str
    identity: Optional[str] = None
    indicator: Optional[str] = None
    classification: str = "THREAT_DETECTION"
    status: Literal["NEW", "CLUSTERED", "TRIAGED", "SUPPRESSED", "CLOSED"] = "NEW"
    fingerprint: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class AlertClusterDTO(BaseModel):
    cluster_id: str = Field(default_factory=lambda: f"clst_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    alert_ids: List[str] = Field(default_factory=list)
    shared_indicator: Optional[str] = None
    shared_asset: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class AlertPriorityDTO(BaseModel):
    alert_id: str
    priority_score: float = Field(..., ge=0.0, le=100.0)
    severity_weight: float = 0.35
    asset_criticality_weight: float = 0.25
    exploitability_weight: float = 0.15
    exposure_weight: float = 0.10
    threat_intel_weight: float = 0.10
    control_health_weight: float = 0.05
    reasoning_breakdown: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class FalsePositiveRecordDTO(BaseModel):
    rule_id: str
    tenant_id: str
    status: Literal["CONFIRMED_BENIGN", "FALSE_POSITIVE", "TRUE_POSITIVE", "INCONCLUSIVE"]
    evidence_ids: List[str] = Field(default_factory=list)
    learned_patterns: List[str] = Field(default_factory=list)
    human_validated: bool = True
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Incident State Machine & Blast Radius DTOs
# ============================================================================

class IncidentStateMachineDTO(BaseModel):
    incident_id: str
    current_state: SOCIncidentStateLiteral = "NEW"
    state_history: List[Dict[str, Any]] = Field(default_factory=list)
    allowed_next_states: List[SOCIncidentStateLiteral] = Field(default_factory=list)
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class IncidentBlastRadiusDTO(BaseModel):
    incident_id: str
    observed_impact_assets: List[str] = Field(default_factory=list)
    potential_impact_assets: List[str] = Field(default_factory=list)
    affected_services: List[str] = Field(default_factory=list)
    affected_identities: List[str] = Field(default_factory=list)
    business_functions: List[str] = Field(default_factory=list)
    blast_radius_score: float = Field(default=25.0, ge=0.0, le=100.0)

    model_config = ConfigDict(frozen=True)


class IncidentCommandStructureDTO(BaseModel):
    incident_id: str
    incident_commander: str
    technical_lead: str
    comms_lead: str
    recovery_lead: str
    security_analyst: str
    assigned_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Response Plans, Playbooks & Validation DTOs
# ============================================================================

class ResponsePlanDetailedDTO(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:10]}")
    incident_id: str
    objective: str
    steps: List[str] = Field(default_factory=list)
    target: str
    expected_outcome: str
    risk_score: float = 15.0
    rollback_steps: List[str] = Field(default_factory=list)
    verification_method: str = "QUERY_PROVIDER_API"
    required_approval_tier: str = "TIER_2_FOUR_EYES"
    is_safe: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class PlaybookNodeDTO(BaseModel):
    node_id: str
    node_type: PlaybookNodeTypeLiteral
    name: str
    config: Dict[str, Any] = Field(default_factory=dict)
    next_node_ids: List[str] = Field(default_factory=list)
    requires_approval: bool = False
    timeout_seconds: int = 300

    model_config = ConfigDict(frozen=True)


class SecurePlaybookDTO(BaseModel):
    playbook_id: str = Field(default_factory=lambda: f"pb_{uuid.uuid4().hex[:10]}")
    tenant_id: str = "default_tenant"
    version: int = 1
    name: str
    owner: str = "usr_soc_lead"
    approval_status: Literal["DRAFT", "PENDING_APPROVAL", "APPROVED", "REJECTED"] = "APPROVED"
    test_status: Literal["UNTESTED", "SIMULATION_PASSED", "VERIFIED"] = "SIMULATION_PASSED"
    nodes: List[PlaybookNodeDTO] = Field(default_factory=list)
    rollback_strategy: List[str] = Field(default_factory=list)
    last_reviewed: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class PlaybookValidationResultDTO(BaseModel):
    playbook_id: str
    is_valid: bool
    unreachable_nodes: List[str] = Field(default_factory=list)
    has_infinite_loop: bool = False
    missing_approvals: List[str] = Field(default_factory=list)
    unsafe_actions: List[str] = Field(default_factory=list)
    missing_verification: List[str] = Field(default_factory=list)
    missing_timeouts: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Action Execution, Verification & Guardrails DTOs
# ============================================================================

class ResponseActionExecutionDTO(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:10]}")
    incident_id: str
    target: str
    provider: str
    idempotency_key: str = Field(default_factory=lambda: f"idemp_{uuid.uuid4().hex[:12]}")
    action_state: SOCActionStateLiteral = "REQUESTED"
    execution_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    retries_count: int = 0
    requester_id: str = "usr_analyst_01"
    approver_id: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class ActionVerificationResultDTO(BaseModel):
    action_id: str
    verification_status: ActionVerificationStatusLiteral = "VERIFIED_SUCCESS"
    expected_state: str
    actual_state: str
    divergence_detected: bool = False
    evidence_reference: Optional[str] = None
    verified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class ResponseActionBudgetDTO(BaseModel):
    tenant_id: str
    max_actions_per_hour: int = 50
    current_action_count: int = 0
    max_blast_radius_pct: float = 20.0
    max_affected_assets: int = 5
    budget_exceeded: bool = False

    model_config = ConfigDict(frozen=True)


class AutomationGuardrailsDTO(BaseModel):
    tenant_id: str
    is_paused: bool = False
    paused_by: Optional[str] = None
    pause_reason: Optional[str] = None
    circuit_breaker_tripped: bool = False
    max_execution_depth: int = 10
    execution_timeout_seconds: int = 600

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Case, Task, Communications & Scorecard DTOs
# ============================================================================

class IncidentTaskDTO(BaseModel):
    task_id: str = Field(default_factory=lambda: f"tsk_{uuid.uuid4().hex[:8]}")
    incident_id: str
    title: str
    owner: str
    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    status: Literal["TODO", "IN_PROGRESS", "BLOCKED", "COMPLETED", "CANCELLED"] = "TODO"
    due_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence_ids: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class SecurityCaseDTO(BaseModel):
    case_id: str = Field(default_factory=lambda: f"case_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    title: str
    incident_ids: List[str] = Field(default_factory=list)
    alert_ids: List[str] = Field(default_factory=list)
    tasks: List[IncidentTaskDTO] = Field(default_factory=list)
    status: Literal["OPEN", "IN_INVESTIGATION", "PENDING_RECOVERY", "RESOLVED", "CLOSED"] = "OPEN"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class IncidentCommunicationDTO(BaseModel):
    communication_id: str = Field(default_factory=lambda: f"comm_{uuid.uuid4().hex[:8]}")
    incident_id: str
    audience: Literal["SOC_UPDATE", "TECHNICAL_UPDATE", "MANAGEMENT_UPDATE", "EXECUTIVE_UPDATE"]
    content: str
    label: Literal["CONFIRMED", "SUSPECTED", "UNKNOWN"] = "CONFIRMED"
    contains_secrets: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class SOCScorecardDTO(BaseModel):
    tenant_id: str
    alert_volume: int = 1420
    true_positive_rate_pct: float = 94.5
    false_positive_rate_pct: float = 5.5
    mttd_minutes: float = 4.2
    mtta_minutes: float = 2.1
    mttr_minutes: float = 18.5
    mean_containment_minutes: float = 6.4
    verification_rate_pct: float = 98.2
    automation_rate_pct: float = 84.0
    failed_action_count: int = 0
    sla_compliance_pct: float = 99.4
    scorecard_grade: str = "EXCELLENT"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
