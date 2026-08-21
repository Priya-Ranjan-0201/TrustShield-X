"""
TruthShield X — Autonomous Cyber Defense & Digital Trust Models (Phase 5 & Phase 30).

Strictly typed Pydantic models for Explainable Decision Records, Closed-Loop Defensive Learning,
Autonomy Governance Levels, Alert/Detection/Response Optimization, Model Governance, Verification,
and Phase 5 SOAR Response Planning and Simulation.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Phase 5 Enums & Literals
# ============================================================================

ExecutionStateLiteral = Literal[
    "CREATED",
    "SIMULATED",
    "AWAITING_APPROVAL",
    "APPROVED",
    "EXECUTING",
    "EXECUTED",
    "VERIFYING",
    "VERIFIED",
    "FAILED",
    "EXECUTION_UNKNOWN",
    "ROLLED_BACK",
    "ROLLBACK_FAILED",
    "ROLLBACK_UNAVAILABLE",
    "CANCELLED",
]

SafetyClassificationLiteral = Literal[
    "SAFE_NO_SIDE_EFFECTS",
    "REVERSIBLE_WITH_IMPACT",
    "IRREVERSIBLE",
    "UNKNOWN_SIDE_EFFECTS",
    "READ_ONLY",
    "LOW_RISK_MUTATION",
    "HIGH_RISK_MUTATION",
    "DESTRUCTIVE",
]


# ============================================================================
# Phase 5 Models (SOAR, Response Plans, Copilot)
# ============================================================================

class DecisionContextDTO(BaseModel):
    model_config = ConfigDict(extra="allow")

    threat_type: str = "UNKNOWN_THREAT"
    target: str = "127.0.0.1"
    target_type: str = "IP"
    action_type: Optional[str] = None
    severity: str = "HIGH"
    risk_score: float = 85.0
    confidence: float = 0.95
    tenant_id: str = "org_default"
    legal_hold: bool = False
    asset_criticality: Optional[str] = None
    evidence_ids: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DecisionResultDTO(BaseModel):
    model_config = ConfigDict(extra="allow")

    decision: str = "EXECUTE"
    recommended_action: str = "BLOCK_IP"
    target: str = "127.0.0.1"
    safety_classification: str = "SAFE_NO_SIDE_EFFECTS"
    required_approval: bool = False
    rationale: str = "Calculated risk threshold exceeded"
    policy_basis: str = "AUTONOMOUS_DEFENSE_POLICY"
    reason: str = "Standard autonomous defense evaluation."
    confidence: float = 0.95



class ResponsePlanActionDTO(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:8]}")
    action_type: str = "BLOCK_IP"
    target: str = "192.168.1.100"
    target_type: str = "IP"
    safety_classification: SafetyClassificationLiteral = "SAFE_NO_SIDE_EFFECTS"
    risk_level: str = "HIGH"
    approval_required: bool = False
    approval_status: str = "NOT_REQUIRED"
    approval_id: Optional[str] = None
    state: ExecutionStateLiteral = "CREATED"
    dry_run_supported: bool = True
    rollback_supported: bool = True
    idempotency_key: str = Field(default_factory=lambda: f"idem_{uuid.uuid4().hex[:12]}")
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    verified_at: Optional[str] = None
    result_summary: Optional[str] = None
    error_message: Optional[str] = None


class ResponsePlanDTO(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "org_default"
    incident_id: Optional[str] = None
    campaign_id: Optional[str] = None
    title: str = "Automated C2 Mitigation Plan"
    description: str = "Immediate containment for identified C2 beaconing activity"
    risk_score: float = 85.0
    confidence: float = 0.95
    actions: List[ResponsePlanActionDTO] = Field(default_factory=list)
    state: ExecutionStateLiteral = "CREATED"
    requires_human_approval: bool = False
    all_approved: bool = True
    rollback_plan: List[str] = Field(default_factory=list)
    verification_plan: List[str] = Field(default_factory=list)
    expected_outcome: str = "Containment achieved within 60s"
    content_hash: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SimulationResultDTO(BaseModel):
    simulation_id: str = Field(default_factory=lambda: f"sim_{uuid.uuid4().hex[:8]}")
    plan_id: str
    simulated_actions_count: int
    mutations_expected: int = 0
    external_network_calls_blocked: int
    policy_evaluation_passed: bool = True
    side_effects: List[str] = Field(default_factory=list)
    verdict: str = "SIMULATION_PASSED_ZERO_EXTERNAL_MUTATION"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class VerificationResultDTO(BaseModel):
    verification_id: str = Field(default_factory=lambda: f"ver_{uuid.uuid4().hex[:8]}")
    action_id: str
    target: str
    verified_state: str = "CONTAINED"
    empirical_evidence: List[str] = Field(default_factory=list)
    verification_passed: bool = True
    latency_ms: float = 12.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RollbackResultDTO(BaseModel):
    rollback_id: str = Field(default_factory=lambda: f"rb_{uuid.uuid4().hex[:8]}")
    action_id: str
    target: str
    rollback_status: str = "ROLLED_BACK"
    reason: str = "Rollback successful"
    executed_by: str = "SOC_LEAD"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EffectivenessScoreDTO(BaseModel):
    model_config = ConfigDict(extra="allow")

    plan_id: str
    initial_risk: float = 85.0
    residual_risk: float = 15.0
    effectiveness_score: float = 95.0
    containment_speed_ms: float = 450.0
    containment_success_rate: float = 1.0
    time_to_containment_seconds: float = 0.5
    residual_risk_score: float = 15.0
    collateral_disruption_score: float = 0.0
    reversal_count: int = 0
    factors: Dict[str, Any] = Field(default_factory=dict)
    summary: str = "HIGHLY_EFFECTIVE: Rapid threat containment with zero collateral impact and verified risk reduction."
    side_effect_penalty: float = 0.0
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityCopilotQueryDTO(BaseModel):
    query: str
    context: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: str = "org_default"


class SecurityCopilotResponseDTO(BaseModel):
    response: str
    confidence: float = 0.95
    evidence: List[str] = Field(default_factory=list)
    suggested_actions: List[str] = Field(default_factory=list)


# ============================================================================
# Phase 30 Type Literals & Enums
# ============================================================================

DecisionTypeLiteral = Literal[
    "ALERT_PRIORITIZATION",
    "INVESTIGATION_PRIORITY",
    "THREAT_HUNT",
    "DETECTION_TUNING",
    "RESPONSE_RECOMMENDATION",
    "CONTROL_IMPROVEMENT",
    "RECOVERY_RECOMMENDATION",
    "SIMULATION_SELECTION",
    "ESCALATION",
]

ClaimStatusLiteral = Literal[
    "OBSERVED",
    "VERIFIED",
    "SIMULATED",
    "PREDICTED",
    "LEARNED",
    "CANDIDATE",
    "APPROVAL_REQUIRED",
    "APPROVED",
    "DEPLOYED",
    "ROLLED_BACK",
    "OUTCOME_NOT_VERIFIED",
    "LEARNING_CONFLICT",
    "LEARNING_NOT_SUPPORTED",
    "REJECTED",
]

AutonomyLevelLiteral = Literal[
    "LEVEL_0",  # OBSERVE_ONLY
    "LEVEL_1",  # ANALYZE
    "LEVEL_2",  # RECOMMEND
    "LEVEL_3",  # SIMULATE
    "LEVEL_4",  # APPROVAL_CONTROLLED
    "LEVEL_5",  # POLICY_BOUND_AUTOMATION
]

ApplicabilityLiteral = Literal[
    "TENANT_SPECIFIC",
    "ENVIRONMENT_SPECIFIC",
    "PLATFORM_SPECIFIC",
    "GENERIC",
]

ResponseEffectivenessLiteral = Literal[
    "RESPONSE_EFFECTIVE",
    "RESPONSE_PARTIALLY_EFFECTIVE",
    "RESPONSE_INEFFECTIVE",
    "OUTCOME_NOT_VERIFIED",
]

ModelDriftLiteral = Literal[
    "STABLE",
    "FEATURE_DRIFT",
    "PREDICTION_DRIFT",
    "PERFORMANCE_DRIFT",
    "CALIBRATION_DRIFT",
]


# ============================================================================
# Phase 30 Models (Decision Records, Closed-Loop Learning, Governance)
# ============================================================================

class SecurityDecisionRecordDTO(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:8]}")
    decision_type: DecisionTypeLiteral = "RESPONSE_RECOMMENDATION"
    decision_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actor_type: Literal["AI_AGENT", "AUTONOMOUS_ENGINE", "SOC_ANALYST", "INCIDENT_COMMANDER"] = "AUTONOMOUS_ENGINE"
    actor_id: str = "engine_response_opt_01"
    evidence: List[str] = Field(default_factory=lambda: ["Sigma alert C2 burst", "Digital Twin sandbox simulation 85% containment"])
    context: Dict[str, Any] = Field(default_factory=lambda: {"threat": "DarkStorm", "target": "ast_api_gw"})
    policy: str = "POL-AUTONOMOUS-CONTAINMENT-V2"
    recommendation: str = "Apply dynamic rate-limiting on Edge Gateway"
    confidence: float = 0.94
    selected_action: str = "WAF_RATE_LIMIT"
    alternatives: List[str] = Field(default_factory=lambda: ["FULL_ISOLATION", "PASSIVE_MONITORING"])
    expected_outcome: str = "90% reduction in malicious credential-stuffing traffic without dropping benign users"
    actual_outcome: Optional[str] = None
    verification_status: ClaimStatusLiteral = "SIMULATED"
    approval: Optional[str] = "USR_CISO_FOUR_EYES"
    rollback_plan: str = "Revert WAF rate-limit ruleset to baseline"
    autonomy_level: AutonomyLevelLiteral = "LEVEL_4"
    tenant_id: str = "default_tenant"

    model_config = ConfigDict(frozen=True)


class DefensiveLessonDTO(BaseModel):
    lesson_id: str = Field(default_factory=lambda: f"lsn_{uuid.uuid4().hex[:8]}")
    threat_pattern: str = "DarkStorm C2 DNS Tunneling Anomaly"
    environment: str = "Production Kubernetes Ingress"
    recommended_action: str = "Enable early DNS entropy inspection filter"
    expected_gain: str = "Reduces MTTD from 12m to 2m"
    evidence_count: int = 5
    validation_count: int = 3
    confidence: float = 0.95
    applicability: ApplicabilityLiteral = "TENANT_SPECIFIC"
    expiration: str = Field(default_factory=lambda: "2027-01-01T00:00:00Z")
    status: ClaimStatusLiteral = "LEARNED"
    tenant_id: str = "default_tenant"

    model_config = ConfigDict(frozen=True)


class AlertOptimizationDTO(BaseModel):
    total_alerts: int = 150
    deduplicated_alerts: int = 85
    suppressed_alerts: int = 25
    true_positive_rate: float = 0.96
    false_positive_rate: float = 0.04
    optimization_status: str = "OPTIMAL"

    model_config = ConfigDict(frozen=True)


class DetectionOptimizationDTO(BaseModel):
    rule_id: str = "rule_darkstorm_c2_entropy"
    rule_name: str = "DarkStorm DNS High Entropy Detection"
    precision: float = 0.96
    recall: float = 0.92
    detection_latency_ms: float = 45.0
    drift_status: str = "STABLE"
    candidate_rule: Optional[str] = None
    status: ClaimStatusLiteral = "DEPLOYED"

    model_config = ConfigDict(frozen=True)


class ThreatHuntingOptimizationDTO(BaseModel):
    hunt_id: str = Field(default_factory=lambda: f"hunt_opt_{uuid.uuid4().hex[:8]}")
    hypothesis: str = "Attackers are utilizing secondary DNS resolvers to bypass primary WAF inspection"
    data_sources: List[str] = Field(default_factory=lambda: ["CoreDNS logs", "Zeek DNS records"])
    novelty_score: float = 0.88
    priority: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "HIGH"
    status: ClaimStatusLiteral = "CANDIDATE"

    model_config = ConfigDict(frozen=True)


class ResponseOptimizationDTO(BaseModel):
    response_id: str = "rsp_darkstorm_waf"
    playbook_name: str = "DarkStorm Credential Stuffing Joint Mitigation Playbook"
    containment_time_sec: float = 42.0
    recovery_time_sec: float = 120.0
    effectiveness: ResponseEffectivenessLiteral = "RESPONSE_EFFECTIVE"
    side_effects: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class ControlOptimizationDTO(BaseModel):
    control_id: str = "ctrl_ingress_waf"
    control_domain: Literal["PREVENTION", "DETECTION", "RESPONSE", "RECOVERY"] = "PREVENTION"
    effectiveness_score: float = 0.95
    gap_description: Optional[str] = None
    candidate_remediation: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class AdaptivePolicyDTO(BaseModel):
    policy_id: str = "pol_dynamic_rate_limit"
    name: str = "Dynamic Ingress WAF Rate Limiting Policy"
    risk_score: float = 0.15
    is_weakened: bool = False
    status: Literal["ACTIVE", "PENDING_APPROVAL", "BLOCKED"] = "ACTIVE"

    model_config = ConfigDict(frozen=True)


class SecurityExperimentDTO(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:8]}")
    hypothesis: str = "Increasing DNS entropy sensitivity threshold decreases false alarms without missing true C2"
    baseline_strategy: str = "Entropy Threshold 4.2"
    candidate_strategy: str = "Entropy Threshold 3.9"
    metrics: Dict[str, float] = Field(default_factory=lambda: {"fp_reduction": 0.15, "precision": 0.97})
    status: Literal["RUNNING", "COMPLETED", "STOPPED", "ROLLED_BACK"] = "COMPLETED"
    rollback_procedure: str = "Revert entropy parameter to 4.2"

    model_config = ConfigDict(frozen=True)


class ModelGovernanceDTO(BaseModel):
    model_id: str = "mdl_c2_neural_classifier"
    version: str = "2.1.0"
    owner: str = "AI_SECURITY_TEAM"
    purpose: str = "Multi-modal DNS & Netflow C2 detection"
    precision: float = 0.97
    recall: float = 0.95
    f1_score: float = 0.96
    drift_status: ModelDriftLiteral = "STABLE"
    status: Literal["DEPLOYED", "QUARANTINED", "ROLLED_BACK"] = "DEPLOYED"

    model_config = ConfigDict(frozen=True)


class ActionVerificationDTO(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:8]}")
    target: str = "ast_api_gw"
    intended_outcome: str = "WAF rate-limiting applied"
    observed_outcome: str = "WAF rate-limiting operational; 0 collateral user drop"
    is_verified: bool = True
    verification_status: ClaimStatusLiteral = "VERIFIED"

    model_config = ConfigDict(frozen=True)


class RollbackRecordDTO(BaseModel):
    rollback_id: str = Field(default_factory=lambda: f"rb_{uuid.uuid4().hex[:8]}")
    target_entity: str = "rule_darkstorm_c2_entropy"
    reverted_change: str = "Reverted candidate rule back to version 1.0.0"
    is_verified: bool = True
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class AutonomousDefenseScorecardDTO(BaseModel):
    autonomy_level: AutonomyLevelLiteral = "LEVEL_4"
    active_decisions_count: int = 12
    pending_approvals_count: int = 1
    active_experiments_count: int = 1
    verified_lessons_count: int = 5
    detection_quality_score: float = 0.96
    response_effectiveness_score: float = 0.95
    system_health: str = "HEALTHY"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
