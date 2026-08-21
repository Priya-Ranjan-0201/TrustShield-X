"""
TruthShield X — Phase 17 Autonomous Cyber Defense, Adaptive Security Mesh,
Real-Time Exposure Control & Closed-Loop Defense Models.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Phase 17 Type Literals
# ============================================================================

DefensePostureStateLiteral = Literal[
    "NORMAL",
    "ELEVATED",
    "HIGH_ALERT",
    "CRITICAL",
    "CONTAINMENT",
    "RECOVERY",
    "DEGRADED",
    "UNKNOWN",
]

ActionClassificationLiteral = Literal[
    "OBSERVATION_ONLY",
    "MONITORING_CHANGE",
    "DETECTION_CHANGE",
    "POLICY_CHANGE",
    "ACCESS_CHANGE",
    "NETWORK_CONTROL",
    "ASSET_ISOLATION",
    "CREDENTIAL_CONTROL",
    "SERVICE_CONTROL",
    "RECOVERY_ACTION",
]

AutomationLevelLiteral = Literal[
    "LEVEL_0_MANUAL",
    "LEVEL_1_RECOMMENDATION",
    "LEVEL_2_HUMAN_APPROVAL",
    "LEVEL_3_PREAUTHORIZED_CONTROLLED_AUTOMATION",
    "LEVEL_4_AUTOMATIC_SAFE_ACTION",
]

CircuitBreakerStateLiteral = Literal[
    "CLOSED",
    "OPEN",
    "HALF_OPEN",
]

DriftSeverityLiteral = Literal[
    "INFORMATIONAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]

DefenseDecisionStatusLiteral = Literal[
    "NO_ACTION",
    "MONITOR",
    "RECOMMEND",
    "APPROVAL_REQUIRED",
    "EXECUTE_ALLOWED",
    "BLOCKED",
]

VerificationOutcomeLiteral = Literal[
    "VERIFIED",
    "VERIFICATION_FAILED",
    "SIMULATION_PRODUCTION_DIVERGENCE",
    "NOT_VERIFIED",
]


# ============================================================================
# Posture & Environment Models
# ============================================================================

class DefensePostureDTO(BaseModel):
    """Real-Time Adaptive Defense Posture (Section 3-4)."""
    model_config = ConfigDict(from_attributes=True)

    posture_id: str = Field(default_factory=lambda: f"pos_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    environment: str = "PRODUCTION"
    security_state: DefensePostureStateLiteral = "NORMAL"
    threat_level: Literal["LOW", "ELEVATED", "HIGH", "CRITICAL"] = "LOW"
    exposure_level: float = 0.15  # 0.0 to 1.0
    control_health: float = 0.95  # 0.0 to 1.0
    attack_surface_score: float = 24.5  # 0 to 100
    active_campaigns_count: int = 0
    active_incidents_count: int = 0
    critical_assets_count: int = 12
    policy_state: str = "ENFORCING"
    last_verified: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    posture_version: int = 1


class SecurityEnvironmentSnapshotDTO(BaseModel):
    """Continuous Security Environment Snapshot (Section 5-6)."""
    model_config = ConfigDict(from_attributes=True)

    snapshot_id: str = Field(default_factory=lambda: f"env_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    assets: List[str] = Field(default_factory=list)
    services: List[str] = Field(default_factory=list)
    identities: List[str] = Field(default_factory=list)
    endpoints: List[str] = Field(default_factory=list)
    apis: List[str] = Field(default_factory=list)
    cloud_resources: List[str] = Field(default_factory=list)
    network_boundaries: List[str] = Field(default_factory=list)
    security_controls: List[str] = Field(default_factory=list)
    vulnerabilities: List[str] = Field(default_factory=list)
    exposures: List[str] = Field(default_factory=list)
    active_threats: List[str] = Field(default_factory=list)
    version: int = 1
    captured_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Security Drift & Exposure Control
# ============================================================================

class AdaptiveDriftEventDTO(BaseModel):
    """Adaptive Security Drift Event (Section 7-8)."""
    model_config = ConfigDict(from_attributes=True)

    drift_id: str = Field(default_factory=lambda: f"drf_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    drift_type: Literal[
        "CONFIGURATION_DRIFT",
        "POLICY_DRIFT",
        "IDENTITY_DRIFT",
        "EXPOSURE_DRIFT",
        "CONTROL_DRIFT",
        "INFRASTRUCTURE_DRIFT",
        "MODEL_DRIFT",
    ] = "CONFIGURATION_DRIFT"
    affected_asset: str
    previous_state: str
    current_state: str
    severity: DriftSeverityLiteral = "MEDIUM"
    exploitability_factor: float = 0.5
    business_criticality: str = "HIGH"
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AttackSurfaceScoreDTO(BaseModel):
    """Multi-Dimensional Attack Surface Scorecard (Section 11)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    exposed_assets_score: float = 20.0
    exposed_services_score: float = 15.0
    vulnerabilities_score: float = 25.0
    identity_exposure_score: float = 10.0
    third_party_exposure_score: float = 12.0
    cloud_exposure_score: float = 18.0
    control_coverage_score: float = 88.0
    overall_attack_surface_score: float = 24.5  # Lower is safer
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Adaptive Recommendations & Safe Actions
# ============================================================================

class AdaptiveControlRecommendationDTO(BaseModel):
    """Evidence-Referenced Adaptive Defense Recommendation (Section 12-14)."""
    model_config = ConfigDict(from_attributes=True)

    recommendation_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    title: str
    action_classification: ActionClassificationLiteral = "MONITORING_CHANGE"
    target_resource: str
    target_type: str = "ENDPOINT"
    automation_level: AutomationLevelLiteral = "LEVEL_2_HUMAN_APPROVAL"
    risk_reduction_score: float = 0.75
    collateral_risk_score: float = 0.10
    evidence_references: List[str] = Field(default_factory=list)
    reasoning: str = ""
    is_time_bounded: bool = True
    duration_minutes: int = 60
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SafeDefenseActionDefinitionDTO(BaseModel):
    """Pre-Authorized Safe Action Catalog Entry (Section 15-16)."""
    model_config = ConfigDict(from_attributes=True)

    action_type: str
    description: str
    scope: str
    allowed_target_patterns: List[str] = Field(default_factory=list)
    prohibited_targets: List[str] = Field(default_factory=lambda: [
        "127.0.0.1", "localhost", "10.0.0.1", "trustshield.internal",
        "root", "admin", "production-db-primary"
    ])
    preconditions: List[str] = Field(default_factory=list)
    requires_approval: bool = False
    is_reversible: bool = True
    rollback_handler: str = "DEFAULT_ROLLBACK"
    rate_limit_per_hour: int = 30
    owner_team: str = "SOC_AUTOMATION"


# ============================================================================
# Simulation, Decision & Circuit Breaker
# ============================================================================

class DefenseSimulationResultDTO(BaseModel):
    """Digital Twin Pre-Execution Simulation Result (Section 18-19)."""
    model_config = ConfigDict(from_attributes=True)

    simulation_id: str = Field(default_factory=lambda: f"sim_{uuid.uuid4().hex[:8]}")
    action_id: str
    simulated_before_state: Dict[str, Any] = Field(default_factory=dict)
    simulated_after_state: Dict[str, Any] = Field(default_factory=dict)
    state_delta: Dict[str, Any] = Field(default_factory=dict)
    risk_reduction_percentage: float = 65.0
    collateral_service_impact: Literal["NONE", "NEGLIGIBLE", "MODERATE", "SEVERE"] = "NEGLIGIBLE"
    dependency_impact_count: int = 0
    is_reversible: bool = True
    is_simulated_label: bool = True  # Mandatory invariant
    simulated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DefenseDecisionRecordDTO(BaseModel):
    """Auditable Multi-Signal Defense Decision (Section 20-22, 61)."""
    model_config = ConfigDict(from_attributes=True)

    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    trigger_type: str
    status: DefenseDecisionStatusLiteral = "RECOMMEND"
    proposed_action: str
    target: str
    evidence_confidence: float = 0.85
    threat_confidence: float = 0.80
    action_confidence: float = 0.90
    simulation_confidence: float = 0.88
    explanation: Dict[str, str] = Field(default_factory=dict)  # Why, Evidence, Risk, Side Effects
    required_authorization: str = "FOUR_EYES_APPROVAL"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DefenseCircuitBreakerDTO(BaseModel):
    """Automated Defense Circuit Breaker State (Section 48-49)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    state: CircuitBreakerStateLiteral = "CLOSED"
    consecutive_failures: int = 0
    failure_threshold: int = 3
    cooldown_seconds: int = 300
    last_tripped_at: Optional[str] = None
    trip_reason: Optional[str] = None
    kill_switch_active: bool = False  # Global emergency halt


class AutomationControlStateDTO(BaseModel):
    """Automation Control Center State (Section 65)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    automation_enabled: bool = True
    kill_switch_active: bool = False
    paused_action_classes: List[ActionClassificationLiteral] = Field(default_factory=list)
    active_automated_actions_count: int = 0
    circuit_breaker_state: CircuitBreakerStateLiteral = "CLOSED"
    last_modified_by: str = "SYSTEM"
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Change Record, Verification & Effectiveness
# ============================================================================

class DefenseChangeRecordDTO(BaseModel):
    """Defense Change Management Record (Section 51-54)."""
    model_config = ConfigDict(from_attributes=True)

    change_id: str = Field(default_factory=lambda: f"chg_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    action_type: str
    target: str
    reason: str
    evidence_references: List[str] = Field(default_factory=list)
    authorization_record: Dict[str, Any] = Field(default_factory=dict)
    executor: str = "SOC_AUTOMATION"
    execution_status: Literal["SCHEDULED", "EXECUTING", "SUCCEEDED", "FAILED", "ROLLED_BACK"] = "SCHEDULED"
    verification_status: VerificationOutcomeLiteral = "NOT_VERIFIED"
    rollback_state: Dict[str, Any] = Field(default_factory=dict)
    is_time_bounded: bool = False
    expires_at: Optional[str] = None
    executed_at: Optional[str] = None
    verified_at: Optional[str] = None


class DefenseEffectivenessScoreDTO(BaseModel):
    """Post-Adaptation Defense Effectiveness Scorecard (Section 55-56)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    action_id: str
    threat_reduction_score: float = 85.0
    exposure_reduction_score: float = 70.0
    control_improvement_score: float = 90.0
    service_stability_score: float = 98.0
    overall_effectiveness: float = 85.75
    residual_risk_score: float = 12.0
    measured_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Graph & Center Summary
# ============================================================================

class AdaptiveDefenseGraphDTO(BaseModel):
    """Adaptive Defense Knowledge Graph (Section 60)."""
    model_config = ConfigDict(from_attributes=True)

    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    total_mitigations: int = 0
    total_protected_assets: int = 0


class AdaptiveDefenseCenterSummaryDTO(BaseModel):
    """Aggregated Adaptive Defense Center Dashboard Summary (Section 62)."""
    model_config = ConfigDict(from_attributes=True)

    current_posture: DefensePostureStateLiteral = "NORMAL"
    threat_level: str = "LOW"
    attack_surface_score: float = 24.5
    control_health: float = 95.0
    active_adaptations_count: int = 0
    pending_approvals_count: int = 0
    failed_adaptations_count: int = 0
    circuit_breaker_status: CircuitBreakerStateLiteral = "CLOSED"
    kill_switch_active: bool = False
    average_effectiveness: float = 88.5
    residual_risk_score: float = 12.0
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
