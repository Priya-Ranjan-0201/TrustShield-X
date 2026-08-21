"""
TruthShield X — Cyber Resilience & Autonomous Recovery Models (Phase 23).

Strictly typed Pydantic models for Resilience Assets, Business Services, Dependency Graphs,
Gaps, Backup Validations, RPO/RTO Metrics, Recovery Plans, Steps, Executions, Verifications,
Business Workflows, DR Drills, Drift, Continuous Validation, and Resilience Scorecards.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 23)
# ============================================================================

ResilienceAssetTypeLiteral = Literal[
    "DATABASE",
    "APPLICATION",
    "STORAGE",
    "NETWORK",
    "IDENTITY",
    "EXTERNAL_DEPENDENCY",
]

ResilienceCriticalityLiteral = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
]

RecoveryStrategyLiteral = Literal[
    "RESTORE_FROM_BACKUP",
    "FAILOVER",
    "REBUILD",
    "REPLICATE",
    "ISOLATE_AND_RECOVER",
    "SERVICE_DEGRADATION",
    "MANUAL_RECOVERY",
    "ALTERNATE_SERVICE",
]

ResilienceMaturityLevelLiteral = Literal[
    "LEVEL_0_UNKNOWN",
    "LEVEL_1_DOCUMENTED",
    "LEVEL_2_IMPLEMENTED",
    "LEVEL_3_TESTED",
    "LEVEL_4_MEASURED",
    "LEVEL_5_CONTINUOUSLY_VALIDATED",
]

DrillTypeLiteral = Literal[
    "DATABASE_RESTORE",
    "SERVICE_FAILOVER",
    "CACHE_FAILURE",
    "QUEUE_FAILURE",
    "WORKER_FAILURE",
    "REGION_FAILURE",
    "IDENTITY_FAILURE",
    "APPLICATION_FAILURE",
    "MULTI_DEPENDENCY_FAILURE",
]

RecoveryExecutionStateLiteral = Literal[
    "REQUESTED",
    "APPROVED",
    "EXECUTING",
    "EXECUTED",
    "VERIFYING",
    "VERIFIED",
    "PARTIAL",
    "FAILED",
    "ROLLED_BACK",
    "UNKNOWN",
    "NOT_VERIFIED",
]


# ============================================================================
# Asset & Business Service Models
# ============================================================================

class ResilienceAssetDTO(BaseModel):
    asset_id: str = Field(default_factory=lambda: f"ast_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    asset_type: ResilienceAssetTypeLiteral = "APPLICATION"
    name: str
    criticality: ResilienceCriticalityLiteral = "HIGH"
    owner: str = "usr_sre_lead"
    environment: Literal["PRODUCTION", "STAGING", "SANDBOX"] = "PRODUCTION"
    dependencies: List[str] = Field(default_factory=list)
    recovery_priority: int = 1
    recovery_strategy: RecoveryStrategyLiteral = "RESTORE_FROM_BACKUP"
    backup_strategy: str = "HOURLY_INCREMENTAL_DAILY_FULL"
    redundancy: Literal["MULTI_AZ", "ACTIVE_PASSIVE", "ACTIVE_ACTIVE", "SINGLE_INSTANCE"] = "MULTI_AZ"
    last_validation: Optional[str] = None
    current_health: Literal["HEALTHY", "DEGRADED", "FAILED", "UNKNOWN"] = "HEALTHY"

    model_config = ConfigDict(frozen=True)


class BusinessServiceDTO(BaseModel):
    service_id: str = Field(default_factory=lambda: f"svc_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    name: str
    criticality: ResilienceCriticalityLiteral = "CRITICAL"
    dependencies: List[str] = Field(default_factory=list)
    supporting_assets: List[str] = Field(default_factory=list)
    recovery_priority: int = 1
    target_RTO_minutes: int = 30
    target_RPO_minutes: int = 15
    validation_requirements: List[str] = Field(default_factory=list)
    current_status: Literal["OPERATIONAL", "DEGRADED", "RECOVERING", "OFFLINE"] = "OPERATIONAL"

    model_config = ConfigDict(frozen=True)


class ServiceDependencyGraphDTO(BaseModel):
    graph_id: str = Field(default_factory=lambda: f"rdg_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    single_points_of_failure: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Resilience Gaps, Backups & RPO/RTO
# ============================================================================

class ResilienceGapDTO(BaseModel):
    gap_id: str = Field(default_factory=lambda: f"gap_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    gap_type: Literal[
        "MISSING_BACKUP", "STALE_BACKUP", "UNTESTED_BACKUP",
        "MISSING_REDUNDANCY", "UNDOCUMENTED_DEPENDENCY", "UNSUPPORTED_RECOVERY_PATH",
        "UNVERIFIED_FAILOVER", "EXCESSIVE_RECOVERY_TIME", "MISSING_MONITORING",
        "MISSING_ROLLBACK", "MISSING_OWNERSHIP"
    ]
    severity: ResilienceCriticalityLiteral = "HIGH"
    affected_service: str
    evidence: str
    recommendation: str
    validation_status: Literal["UNRESOLVED", "RESOLVED", "IN_PROGRESS", "ACCEPTED_RISK"] = "UNRESOLVED"

    model_config = ConfigDict(frozen=True)


class BackupValidationDTO(BaseModel):
    backup_id: str = Field(default_factory=lambda: f"bck_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    asset_id: str
    backup_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    age_hours: float = 2.5
    integrity_status: Literal["VERIFIED", "CORRUPTED", "NOT_VERIFIED", "POISONED"] = "VERIFIED"
    checksum_verified: bool = True
    schema_compatible: bool = True
    record_count: int = 150000
    encryption_verified: bool = True
    sandbox_tested: bool = True
    last_tested_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class RTOEngineDTO(BaseModel):
    service_id: str
    target_rto_minutes: int = 30
    observed_recovery_start: Optional[str] = None
    observed_restoration_time: Optional[str] = None
    actual_rto_minutes: Optional[float] = None
    validation_status: Literal["VERIFIED", "NOT_VERIFIED", "EXCEEDED_TARGET"] = "NOT_VERIFIED"
    evidence_reference: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class RPOEngineDTO(BaseModel):
    service_id: str
    target_rpo_minutes: int = 15
    last_valid_state_timestamp: Optional[str] = None
    actual_data_loss_minutes: Optional[float] = None
    validation_status: Literal["VERIFIED", "NOT_VERIFIED", "EXCEEDED_TARGET"] = "NOT_VERIFIED"
    evidence_reference: Optional[str] = None

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Recovery Planning, Execution, Verification & Drills
# ============================================================================

class RecoveryStepDTO(BaseModel):
    step_id: str = Field(default_factory=lambda: f"step_{uuid.uuid4().hex[:8]}")
    step_order: int
    target: str
    action: str
    prerequisite_steps: List[str] = Field(default_factory=list)
    expected_outcome: str
    is_automated: bool = True
    execution_state: RecoveryExecutionStateLiteral = "REQUESTED"

    model_config = ConfigDict(frozen=True)


class RecoveryPlanDTO(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"recplan_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    title: str
    objective: str
    affected_services: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    recovery_order: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    steps: List[RecoveryStepDTO] = Field(default_factory=list)
    rollback_steps: List[str] = Field(default_factory=list)
    approval_tier: Literal["AUTOMATED_SAFE", "TIER_1_LEAD", "TIER_2_FOUR_EYES"] = "TIER_2_FOUR_EYES"
    is_approved: bool = False
    approver_id: Optional[str] = None
    estimated_duration_minutes: int = 25
    target_RTO_minutes: int = 30
    target_RPO_minutes: int = 15
    owner: str = "usr_dr_commander"
    drift_status: Literal["CURRENT", "OUTDATED"] = "CURRENT"

    model_config = ConfigDict(frozen=True)


class RecoveryActionExecutionDTO(BaseModel):
    recovery_action_id: str = Field(default_factory=lambda: f"ract_{uuid.uuid4().hex[:8]}")
    plan_id: str
    step_id: str
    target: str
    action: str
    authorization_token: str
    execution_state: RecoveryExecutionStateLiteral = "EXECUTED"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    result_details: str = "Step executed successfully against runtime provider adapter."

    model_config = ConfigDict(frozen=True)


class RecoveryVerificationDTO(BaseModel):
    verification_id: str = Field(default_factory=lambda: f"rver_{uuid.uuid4().hex[:8]}")
    recovery_action_id: str
    target: str
    verification_status: Literal["VERIFIED", "PARTIAL", "FAILED", "RECOVERY_INCOMPLETE", "RECOVERY_DIVERGENCE", "NOT_VERIFIED"] = "VERIFIED"
    divergence_detected: bool = False
    evidence_reference: str = Field(default_factory=lambda: f"ev_ver_{uuid.uuid4().hex[:8]}")
    verified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class BusinessValidationResultDTO(BaseModel):
    validation_id: str = Field(default_factory=lambda: f"bval_{uuid.uuid4().hex[:8]}")
    service_id: str
    workflow_name: str = "SYNTHETIC_E2E_CHECKOUT_TRANSACTION"
    workflow_status: Literal["VALIDATED", "FAILED", "NOT_VERIFIED"] = "VALIDATED"
    latency_ms: float = 180.0
    records_verified: int = 42
    validated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class DisasterRecoveryDrillDTO(BaseModel):
    drill_id: str = Field(default_factory=lambda: f"drill_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    drill_type: DrillTypeLiteral = "DATABASE_RESTORE"
    environment: Literal["ISOLATED_SANDBOX", "STAGING"] = "ISOLATED_SANDBOX"
    scope: str = "SANDBOX_CHECKOUT_RESTORE"
    status: Literal["SCHEDULED", "RUNNING", "COMPLETED", "ABORTED", "FAILED"] = "COMPLETED"
    abort_reason: Optional[str] = None
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    measured_rto_minutes: float = 14.5
    measured_rpo_minutes: float = 4.2
    evidence_ids: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Drift & Resilience Scorecard
# ============================================================================

class RecoveryDriftDTO(BaseModel):
    drift_id: str = Field(default_factory=lambda: f"drift_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    component_type: Literal["INFRASTRUCTURE", "DEPENDENCY", "BACKUP_SCHEDULE", "RECOVERY_PLAN"]
    description: str
    drift_detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    impact_assessment: str = "Recovery Plan marked OUTDATED due to new unmapped PostgreSQL replica."
    is_reconciled: bool = False

    model_config = ConfigDict(frozen=True)


class ResilienceScorecardDTO(BaseModel):
    tenant_id: str = "default_tenant"
    overall_score: float = 93.8
    recoverability_score: float = 95.0
    redundancy_score: float = 92.0
    backup_health_score: float = 98.5
    recovery_validation_score: float = 91.0
    dependency_resilience_score: float = 90.0
    detection_resilience_score: float = 94.5
    response_resilience_score: float = 96.0
    maturity_level: ResilienceMaturityLevelLiteral = "LEVEL_5_CONTINUOUSLY_VALIDATED"
    scorecard_grade: Literal["EXCELLENT", "ADEQUATE", "NEEDS_IMPROVEMENT", "CRITICAL_RISK"] = "EXCELLENT"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
