"""
TruthShield X — Autonomous Security Engineering Models (Phase 25).

Strictly typed Pydantic models for Security Improvements, Security Gaps, Root Cause Analysis,
Change Impact Analysis, Digital Twin Simulations, Rollout Deployments, Rollbacks,
Outcome Measurements, Security Experiments, Incident Learnings, and Autonomy Governance.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 25)
# ============================================================================

ImprovementCategoryLiteral = Literal[
    "DETECTION",
    "POLICY",
    "ACCESS_CONTROL",
    "MONITORING",
    "ALERTING",
    "SOAR",
    "INCIDENT_RESPONSE",
    "THREAT_HUNTING",
    "THREAT_INTELLIGENCE",
    "RESILIENCE",
    "RECOVERY",
    "DATA_GOVERNANCE",
    "AI_SECURITY",
    "MODEL_CONFIGURATION",
    "PERFORMANCE",
    "SECURITY_CONFIGURATION",
]

ChangeRiskClassificationLiteral = Literal[
    "READ_ONLY",
    "LOW_RISK_REVERSIBLE",
    "MODERATE_RISK",
    "HIGH_RISK",
    "CRITICAL",
]

AutonomyLevelLiteral = Literal[
    "LEVEL_0_RECOMMEND_ONLY",
    "LEVEL_1_SIMULATE",
    "LEVEL_2_HUMAN_APPROVAL",
    "LEVEL_3_CONTROLLED_AUTOMATION",
    "LEVEL_4_CONTINUOUSLY_VERIFIED_AUTOMATION",
]

RolloutStrategyLiteral = Literal[
    "ISOLATED",
    "CANARY",
    "LIMITED",
    "STAGED",
    "FULL",
]

OutcomeStatusLiteral = Literal[
    "IMPROVED",
    "UNCHANGED",
    "DEGRADED",
    "INCONCLUSIVE",
    "NOT_ENOUGH_DATA",
    "NOT_VERIFIED",
]

ImprovementLifecycleStatusLiteral = Literal[
    "RECOMMENDED",
    "SIMULATED",
    "APPROVED",
    "DEPLOYED",
    "VERIFIED",
    "IMPROVED",
    "ROLLED_BACK",
    "FAILED",
]


# ============================================================================
# Security Gap & Root Cause Models
# ============================================================================

class SecurityGapDTO(BaseModel):
    gap_id: str = Field(default_factory=lambda: f"gap_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    source: Literal[
        "FAILED_VALIDATION",
        "SECURITY_INCIDENT",
        "FALSE_POSITIVE",
        "FALSE_NEGATIVE",
        "SECURITY_DRIFT",
        "THREAT_INTELLIGENCE",
        "RESILIENCE_TEST",
        "RECOVERY_TEST",
        "ATTACK_SIMULATION",
        "AUDIT_FINDING",
        "POLICY_CONFLICT",
        "MODEL_DEGRADATION",
    ] = "FAILED_VALIDATION"
    title: str
    description: str
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "HIGH"
    exploitability: float = 0.8
    exposure: float = 0.7
    business_impact: float = 0.85
    likelihood: float = 0.75
    confidence: float = 0.95
    affected_assets: List[str] = Field(default_factory=list)
    remediation_complexity: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    total_gap_score: float = 8.2
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class RootCauseAnalysisDTO(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"rca_{uuid.uuid4().hex[:8]}")
    gap_id: str
    category: Literal["ROOT_CAUSE", "CONTRIBUTING_FACTOR", "CORRELATION", "HYPOTHESIS", "UNKNOWN"] = "ROOT_CAUSE"
    rationale: str
    supporting_evidence: List[str] = Field(default_factory=list)
    identified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Security Improvement & Impact Models
# ============================================================================

class SecurityImprovementDTO(BaseModel):
    improvement_id: str = Field(default_factory=lambda: f"imp_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    category: ImprovementCategoryLiteral = "DETECTION"
    title: str
    description: str
    problem: str
    evidence: List[str] = Field(default_factory=list)
    proposed_change: str
    expected_benefit: str
    expected_risk: str
    confidence: float = 0.95
    impact_score: float = 0.85
    reversibility: Literal["FULLY_REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE"] = "FULLY_REVERSIBLE"
    approval_required: bool = False
    simulation_status: Literal["PENDING", "SIMULATED", "FAILED"] = "PENDING"
    validation_status: Literal["NOT_VERIFIED", "PASSED", "FAILED"] = "NOT_VERIFIED"
    deployment_status: Literal["PENDING", "CANARY_DEPLOYED", "DEPLOYED", "ROLLED_BACK"] = "PENDING"
    outcome_status: OutcomeStatusLiteral = "NOT_VERIFIED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class ImpactAnalysisDTO(BaseModel):
    impact_id: str = Field(default_factory=lambda: f"impct_{uuid.uuid4().hex[:8]}")
    improvement_id: str
    affected_controls: List[str] = Field(default_factory=list)
    affected_services: List[str] = Field(default_factory=list)
    affected_tenants: List[str] = Field(default_factory=list)
    affected_policies: List[str] = Field(default_factory=list)
    affected_detections: List[str] = Field(default_factory=list)
    affected_playbooks: List[str] = Field(default_factory=list)
    affected_recovery_paths: List[str] = Field(default_factory=list)
    blast_radius_score: float = 0.15
    risk_classification: ChangeRiskClassificationLiteral = "LOW_RISK_REVERSIBLE"
    requires_human_approval: bool = False
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Simulation, Rollout, Rollback & Outcome Models
# ============================================================================

class SimulationResultDTO(BaseModel):
    simulation_id: str = Field(default_factory=lambda: f"sim_{uuid.uuid4().hex[:8]}")
    improvement_id: str
    before_state: Dict[str, Any] = Field(default_factory=dict)
    simulated_change: Dict[str, Any] = Field(default_factory=dict)
    after_state: Dict[str, Any] = Field(default_factory=dict)
    digital_twin_verified: bool = True
    status: Literal["SIMULATED_SUCCESS", "SIMULATED_REGRESSION", "SIMULATION_FAILED"] = "SIMULATED_SUCCESS"
    simulated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class DeploymentRolloutDTO(BaseModel):
    deployment_id: str = Field(default_factory=lambda: f"dep_{uuid.uuid4().hex[:8]}")
    improvement_id: str
    tenant_id: str = "default_tenant"
    strategy: RolloutStrategyLiteral = "CANARY"
    previous_state: Dict[str, Any] = Field(default_factory=dict)
    new_state: Dict[str, Any] = Field(default_factory=dict)
    rollback_handle: str = Field(default_factory=lambda: f"rbk_{uuid.uuid4().hex[:8]}")
    deployed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: Literal["CANARY_ACTIVE", "DEPLOYED_FULL", "ROLLED_BACK", "FAILED"] = "CANARY_ACTIVE"

    model_config = ConfigDict(frozen=True)


class RollbackRecordDTO(BaseModel):
    rollback_id: str = Field(default_factory=lambda: f"rbk_rec_{uuid.uuid4().hex[:8]}")
    deployment_id: str
    trigger_reason: str = "Validation regression detected post-canary deployment"
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    rollback_verified: bool = True
    incident_logged: bool = True

    model_config = ConfigDict(frozen=True)


class OutcomeMeasurementDTO(BaseModel):
    outcome_id: str = Field(default_factory=lambda: f"out_{uuid.uuid4().hex[:8]}")
    improvement_id: str
    baseline_metric: float = 0.12  # e.g. 12% false positive rate
    expected_metric: float = 0.02  # e.g. 2% false positive rate
    actual_metric: float = 0.018   # e.g. 1.8% actual post-change rate
    outcome_status: OutcomeStatusLiteral = "IMPROVED"
    risk_reduction_score: float = 8.5
    measured_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Security Experiments, Incident Learning & Governance Models
# ============================================================================

class SecurityExperimentDTO(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    hypothesis: str = "Tuning regex threshold on SQL injection WAF decreases false alerts by 40% without missing true positives."
    baseline: Dict[str, float] = Field(default_factory=lambda: {"false_positive_rate": 0.08, "missed_detections": 0.0})
    treatment: Dict[str, float] = Field(default_factory=lambda: {"false_positive_rate": 0.02, "missed_detections": 0.0})
    metrics: List[str] = Field(default_factory=lambda: ["false_positive_rate", "detection_coverage"])
    duration_hours: int = 24
    expected_result: str = "Lower false positive rate with 0 missed true attacks."
    actual_result: Optional[str] = "False positives reduced by 75%, 0 missed true attacks."
    conclusion: Optional[str] = "Hypothesis validated. Recommended for production deployment."
    status: Literal["PLANNED", "RUNNING", "COMPLETED", "TERMINATED"] = "COMPLETED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class IncidentLearningRecordDTO(BaseModel):
    learning_id: str = Field(default_factory=lambda: f"learn_{uuid.uuid4().hex[:8]}")
    incident_id: str
    detection_eval: str = "Detection rule fired within 12 seconds."
    response_eval: str = "SOAR containment executed cleanly in 45 seconds."
    containment_eval: str = "Host isolation effective."
    recovery_eval: str = "Sandbox restore validated in 110 seconds."
    failures_identified: List[str] = Field(default_factory=list)
    successful_controls: List[str] = Field(default_factory=lambda: ["ctl_tenant_isolation", "ctl_four_eyes_response"])
    lessons_learned: List[str] = Field(default_factory=lambda: ["Add proactive hunting query for credential staging behavior."])
    generated_improvements: List[str] = Field(default_factory=list)
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class AutonomyGovernanceConfigDTO(BaseModel):
    tenant_id: str = "default_tenant"
    autonomy_level: AutonomyLevelLiteral = "LEVEL_3_CONTROLLED_AUTOMATION"
    allowed_actions: List[str] = Field(default_factory=lambda: ["TUNE_DETECTION_THRESHOLD", "OPTIMIZE_ALERT_CORRELATION", "UPDATE_AUDIT_FILTER"])
    prohibited_actions: List[str] = Field(default_factory=lambda: ["DISABLE_AUTH", "BYPASS_FOUR_EYES", "MUTATE_AUDIT_LOG", "WEAKEN_POLICY"])
    blast_radius_threshold: float = 0.30
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
