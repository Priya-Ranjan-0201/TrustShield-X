"""
TruthShield X — Global Security Mission Control Models (Phase 29).

Strictly typed Pydantic models for Unified Security State, Security Event Fabric,
Mission Tasks, Mission Workflows, 8-Dimensional Posture, Incident Command, and System Health.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 29)
# ============================================================================

SecurityEventTypeLiteral = Literal[
    "THREAT_DETECTED",
    "THREAT_UPDATED",
    "CAMPAIGN_UPDATED",
    "VULNERABILITY_DISCOVERED",
    "ASSET_EXPOSED",
    "ALERT_CREATED",
    "ALERT_CORRELATED",
    "INCIDENT_CREATED",
    "INCIDENT_ESCALATED",
    "INCIDENT_CONTAINED",
    "RESPONSE_STARTED",
    "RESPONSE_COMPLETED",
    "RESPONSE_FAILED",
    "RECOVERY_STARTED",
    "RECOVERY_COMPLETED",
    "RECOVERY_FAILED",
    "CONTROL_FAILED",
    "CONTROL_RECOVERED",
    "SECURITY_DRIFT",
    "TWIN_DRIFT",
    "FORECAST_CREATED",
    "EARLY_WARNING",
    "SECURITY_IMPROVEMENT",
    "SIMULATION_COMPLETED",
    "ASSURANCE_FAILURE",
    "COORDINATION_REQUEST",
    "COORDINATION_APPROVED",
    "COORDINATION_BLOCKED",
]

MissionStateStatusLiteral = Literal[
    "OBSERVED",
    "VERIFIED",
    "SIMULATED",
    "PREDICTED",
    "STALE",
    "UNKNOWN",
    "STATE_CONFLICT",
    "BLOCKED",
    "NOT_VERIFIED",
]

TaskStateLiteral = Literal[
    "CREATED",
    "ASSIGNED",
    "IN_PROGRESS",
    "BLOCKED",
    "WAITING_APPROVAL",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
    "VERIFIED",
]

MissionPriorityLiteral = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFORMATIONAL",
]


# ============================================================================
# Security Event Fabric Models
# ============================================================================

class SecurityEventDTO(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    event_type: SecurityEventTypeLiteral = "ALERT_CREATED"
    source: str = "soc_orchestrator"
    tenant_id: str = "default_tenant"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    classification: str = "CONFIDENTIAL"
    payload: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    causation_id: Optional[str] = None
    idempotency_key: str = Field(default_factory=lambda: f"idem_{uuid.uuid4().hex[:12]}")
    confidence: float = 0.95

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Unified Security State & Posture Models
# ============================================================================

class SecurityPostureDTO(BaseModel):
    threat_posture: float = 0.94
    exposure_posture: float = 0.92
    control_posture: float = 0.95
    incident_posture: float = 0.90
    response_posture: float = 0.93
    recovery_posture: float = 0.95
    governance_posture: float = 0.96
    resilience_posture: float = 0.94
    overall_trend: Literal["IMPROVING", "STABLE", "DEGRADING", "UNKNOWN"] = "IMPROVING"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class UnifiedSecurityStateDTO(BaseModel):
    state_id: str = Field(default_factory=lambda: f"state_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    active_threats_count: int = 1
    active_campaigns_count: int = 1
    active_incidents_count: int = 1
    critical_alerts_count: int = 2
    compromised_assets_count: int = 1
    failing_controls_count: int = 0
    active_responses_count: int = 1
    active_recoveries_count: int = 0
    pending_tasks_count: int = 3
    state_conflicts_count: int = 0
    posture_summary: SecurityPostureDTO = Field(default_factory=SecurityPostureDTO)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Mission Tasks & Workflows
# ============================================================================

class MissionTaskDTO(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    title: str = "Investigate DarkStorm C2 DNS Lateral Movement Anomaly"
    task_type: Literal["INVESTIGATE", "VALIDATE", "HUNT", "APPROVE", "CONTAIN", "RECOVER", "VERIFY", "IMPROVE"] = "INVESTIGATE"
    owner: str = "SOC_ANALYST_LEAD"
    priority: MissionPriorityLiteral = "HIGH"
    sla_seconds: float = 1800.0
    dependencies: List[str] = Field(default_factory=list)
    status: TaskStateLiteral = "IN_PROGRESS"
    evidence: List[str] = Field(default_factory=lambda: ["NetFlow burst logs", "Sigma entropy detection alert"])
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class MissionWorkflowDTO(BaseModel):
    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:8]}")
    name: str = "THREAT_TO_INVESTIGATION"
    version: str = "1.0.0"
    trigger_event: SecurityEventTypeLiteral = "EARLY_WARNING"
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    status: Literal["IDLE", "RUNNING", "WAITING_APPROVAL", "COMPLETED", "FAILED", "BLOCKED"] = "RUNNING"
    rollback_procedure: str = "Restore prior baseline routing table"
    requires_four_eyes: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Incident Command, Conflicts & Health
# ============================================================================

class IncidentCommandMissionDTO(BaseModel):
    incident_id: str = "inc_darkstorm_burst"
    title: str = "DarkStorm C2 Gateway Intrusion Incident"
    commander: str = "usr_ciso_alpha"
    severity: MissionPriorityLiteral = "CRITICAL"
    status: str = "CONTAINED"
    timeline_events_count: int = 5
    affected_assets: List[str] = Field(default_factory=lambda: ["ast_api_gw", "ast_auth_cluster"])
    containment_status: str = "CONTAINED"
    response_status: str = "EXECUTED"
    recovery_status: str = "VERIFIED"

    model_config = ConfigDict(frozen=True)


class StateConflictDTO(BaseModel):
    conflict_id: str = Field(default_factory=lambda: f"cnf_{uuid.uuid4().hex[:8]}")
    entity_type: str = "ASSET"
    entity_id: str = "ast_api_gw"
    subsystem_a: str = "SOAR"
    state_a: str = "ISOLATED"
    subsystem_b: str = "ASSET_INVENTORY"
    state_b: str = "ACTIVE_ONLINE"
    status: Literal["STATE_CONFLICT", "RESOLVED"] = "STATE_CONFLICT"
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class MissionControlHealthDTO(BaseModel):
    api_health: str = "HEALTHY"
    db_health: str = "HEALTHY"
    redis_health: str = "HEALTHY"
    queue_health: str = "HEALTHY"
    event_fabric_health: str = "HEALTHY"
    soar_health: str = "HEALTHY"
    digital_twin_health: str = "HEALTHY"
    threat_intel_health: str = "HEALTHY"
    overall_health: str = "HEALTHY"
    monitored_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
