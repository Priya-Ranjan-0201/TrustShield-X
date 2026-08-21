"""
TruthShield X — Phase 18 Autonomous Security Digital Twin, Predictive Cyber Resilience,
Attack-Scenario Simulation & Future-State Security Engine Models.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
import hashlib
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Phase 18 Type Literals
# ============================================================================

DependencyRelationLiteral = Literal[
    "SERVICE_DEPENDS_ON",
    "APPLICATION_USES",
    "IDENTITY_ACCESSES",
    "ASSET_HOSTS",
    "DATA_STORED_ON",
    "CONTROL_PROTECTS",
    "SERVICE_SUPPORTS",
    "RECOVERY_DEPENDS_ON",
]

DependencyConfidenceStateLiteral = Literal[
    "VERIFIED",
    "OBSERVED",
    "INFERRED",
    "UNKNOWN",
]

SimulationLabelLiteral = Literal[
    "SIMULATED",
    "PREDICTED",
    "ESTIMATED",
    "UNKNOWN",
    "DIVERGENCE",
]

InitialConditionLiteral = Literal[
    "CURRENT_STATE",
    "HISTORICAL_STATE",
    "CUSTOM_SANDBOX_STATE",
]

ComparisonClassificationLiteral = Literal[
    "MATCH",
    "PARTIAL_MATCH",
    "DIVERGENCE",
    "UNKNOWN",
]

RoadmapStageLiteral = Literal[
    "NOW",
    "NEXT",
    "LATER",
]


# ============================================================================
# Digital Twin State, Completeness & Confidence Models
# ============================================================================

class TwinStateSnapshotDTO(BaseModel):
    """Digital Twin 2.0 State Snapshot (Section 3)."""
    model_config = ConfigDict(from_attributes=True)

    snapshot_id: str = Field(default_factory=lambda: f"twn_snap_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    environment: str = "PRODUCTION"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_versions: Dict[str, Any] = Field(default_factory=dict)
    asset_count: int = 42
    service_count: int = 18
    identity_count: int = 65
    control_count: int = 24
    exposure_count: int = 7
    threat_count: int = 2
    incident_count: int = 0
    confidence: float = 0.91
    completeness: float = 0.88
    freshness: float = 0.96
    integrity_hash: str = ""


class TwinCompletenessScoreDTO(BaseModel):
    """Multi-Dimensional Twin Completeness Scorecard (Section 4)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    asset_visibility: float = 95.0
    identity_visibility: float = 90.0
    service_visibility: float = 92.0
    dependency_visibility: float = 84.0
    control_visibility: float = 96.0
    threat_visibility: float = 88.0
    business_mapping: float = 78.0
    recovery_mapping: float = 82.0
    overall_completeness: float = 88.125
    measured_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TwinConfidenceScoreDTO(BaseModel):
    """Distinct Confidence, Completeness, and Freshness Tracking (Section 5)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    completeness: float = 88.0
    confidence: float = 91.0
    freshness: float = 96.0
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TwinDriftEventDTO(BaseModel):
    """Reality-to-Twin Drift Event (Section 8)."""
    model_config = ConfigDict(from_attributes=True)

    drift_id: str = Field(default_factory=lambda: f"tdrf_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    drift_type: str = "REALITY_TO_TWIN_DRIFT"
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reality_state: str
    twin_state: str
    severity: Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"] = "MEDIUM"
    status: Literal["DETECTED", "RECONCILED", "IGNORED"] = "DETECTED"


# ============================================================================
# Cyber Dependency Graph & Single Points of Failure
# ============================================================================

class CyberDependencyDTO(BaseModel):
    """Directed Dependency Relationship (Section 9-10)."""
    model_config = ConfigDict(from_attributes=True)

    source_id: str
    target_id: str
    relation_type: DependencyRelationLiteral
    confidence_state: DependencyConfidenceStateLiteral = "VERIFIED"
    confidence_score: float = 0.95
    source: str = "OBSERVED_TELEMETRY"
    last_verified: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CyberDependencyGraphDTO(BaseModel):
    """Topological Cyber Dependency Knowledge Graph."""
    model_config = ConfigDict(from_attributes=True)

    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[CyberDependencyDTO] = Field(default_factory=list)
    total_dependencies: int = 0
    unverified_count: int = 0


class SinglePointOfFailureDTO(BaseModel):
    """Single Point of Failure (SPOF) Assessment (Section 11-12)."""
    model_config = ConfigDict(from_attributes=True)

    resource_id: str
    resource_type: str = "SERVICE"
    impact_severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    cascading_affected_services: List[str] = Field(default_factory=list)
    cascading_affected_controls: List[str] = Field(default_factory=list)
    is_spof: bool = True
    mitigation_suggestion: str = ""


# ============================================================================
# Attack Scenarios, Propagation & What-If Simulations
# ============================================================================

class ScenarioModelDTO(BaseModel):
    """Defensive Simulation Scenario Definition (Section 13-15)."""
    model_config = ConfigDict(from_attributes=True)

    scenario_id: str = Field(default_factory=lambda: f"scen_{uuid.uuid4().hex[:8]}")
    scenario_type: str = "PHISHING_CAMPAIGN"
    initial_conditions: InitialConditionLiteral = "CURRENT_STATE"
    assumptions: List[str] = Field(default_factory=list)
    affected_assets: List[str] = Field(default_factory=list)
    threat_model: str = "EXTERNAL_ADVANCED_THREAT"
    control_dependencies: List[str] = Field(default_factory=list)
    simulation_model: str = "DETERMINISTIC_PROPAGATION_V2"
    confidence: float = 0.88
    limitations: List[str] = Field(default_factory=list)
    is_ai_generated: bool = False
    version: int = 1


class AttackPropagationPathDTO(BaseModel):
    """Discrete Future-State Attack Propagation Steps (Section 16, 30)."""
    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    target_resource: str
    steps: List[Dict[str, Any]] = Field(default_factory=list)  # CURRENT, +1 STEP, +2 STEPS, +3 STEPS
    confidence: float = 0.85
    assumptions: List[str] = Field(default_factory=list)
    label: SimulationLabelLiteral = "PREDICTED"


class WhatIfQueryDTO(BaseModel):
    """What-If Simulation Query (Section 19)."""
    query_type: Literal[
        "ASSET_COMPROMISE",
        "CONTROL_FAILURE",
        "SERVICE_UNAVAILABLE",
        "IDENTITY_COMPROMISE",
        "CAMPAIGN_EXPANSION",
        "DEFENSE_ACTIVATION",
        "RECOVERY_FAILURE",
    ] = "CONTROL_FAILURE"
    target_resource: str
    simulated_change: str


class WhatIfResultDTO(BaseModel):
    """What-If Simulation Outcome."""
    model_config = ConfigDict(from_attributes=True)

    query_id: str = Field(default_factory=lambda: f"wif_{uuid.uuid4().hex[:8]}")
    target_resource: str
    simulated_change: str
    blast_radius_asset_count: int = 3
    affected_services: List[str] = Field(default_factory=list)
    estimated_residual_risk: float = 48.0
    label: SimulationLabelLiteral = "SIMULATED"
    is_simulated: bool = True


class CounterfactualComparisonDTO(BaseModel):
    """Multi-Scenario Counterfactual Blast Radius Comparison (Section 20)."""
    model_config = ConfigDict(from_attributes=True)

    baseline_risk: float = 24.5
    strategy_a_risk: float = 12.0
    strategy_b_risk: float = 18.5
    strategy_c_risk: float = 9.0
    lowest_residual_risk_strategy: str = "STRATEGY_C"
    comparison_label: SimulationLabelLiteral = "SIMULATED"


class DefenseStrategyCandidateDTO(BaseModel):
    """Strategy Candidate for Pareto Frontier Optimization (Section 21-22)."""
    model_config = ConfigDict(from_attributes=True)

    strategy_id: str
    name: str
    risk_reduction: float  # Higher is better (0-100)
    service_disruption: float  # Lower is better (0-100)
    implementation_cost: float  # Lower is better (0-100)
    is_reversible: bool = True
    confidence: float = 0.90
    is_pareto_optimal: bool = False


# ============================================================================
# Resilience Score, Recovery Simulation & RTO/RPO
# ============================================================================

class CyberResilienceScoreDTO(BaseModel):
    """7-Dimensional Cyber Resilience Scorecard (Section 23)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    prevention: float = 88.0
    detection: float = 92.0
    containment: float = 85.0
    recovery: float = 80.0
    adaptability: float = 90.0
    dependency_resilience: float = 82.0
    governance_readiness: float = 94.0
    overall_resilience_score: float = 87.28
    measured_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RecoverySimulationResultDTO(BaseModel):
    """Disaster Recovery & RTO/RPO Simulation Result (Section 24-26)."""
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str = "default_tenant"
    target_rto_minutes: int = 60
    target_rpo_minutes: int = 15
    empirical_rto_minutes: Optional[int] = 75
    empirical_rpo_minutes: Optional[int] = 10
    simulated_rto_minutes: int = 68
    simulated_rpo_minutes: int = 12
    recovery_bottlenecks: List[str] = Field(default_factory=list)
    recovery_path_verified: bool = True
    label: SimulationLabelLiteral = "SIMULATED"


# ============================================================================
# Simulation vs Reality, Calibration & Accuracy
# ============================================================================

class SimulationRealityComparisonDTO(BaseModel):
    """Simulation vs Reality Divergence Comparator (Section 33)."""
    model_config = ConfigDict(from_attributes=True)

    simulation_id: str
    classification: ComparisonClassificationLiteral = "MATCH"
    expected_residual_risk: float = 12.0
    actual_residual_risk: float = 14.5
    error_delta: float = 2.5
    root_cause: Optional[str] = None
    compared_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ModelCalibrationRecordDTO(BaseModel):
    """Continuous Predictive Model Calibration Record (Section 34)."""
    model_config = ConfigDict(from_attributes=True)

    calibration_id: str = Field(default_factory=lambda: f"cal_{uuid.uuid4().hex[:8]}")
    model_version: str = "PREDICTIVE_TWIN_V2"
    historical_predictions_count: int = 150
    average_error_pct: float = 4.2
    calibration_offset: float = -0.05
    last_calibrated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PredictionAccuracyMetricsDTO(BaseModel):
    """Statistical Prediction Accuracy Metrics (Section 35)."""
    model_config = ConfigDict(from_attributes=True)

    precision: float = 0.92
    recall: float = 0.89
    calibration: float = 0.94
    false_positive_rate: float = 0.05
    false_negative_rate: float = 0.08
    sample_size: int = 240
    status: Literal["STATISTICALLY_SUPPORTED", "NOT_ENOUGH_DATA"] = "STATISTICALLY_SUPPORTED"


# ============================================================================
# Recommendations, Roadmap & Dashboard Summary
# ============================================================================

class ResilienceRecommendationDTO(BaseModel):
    """Evidence-Backed Resilience Improvement Recommendation (Section 51-52)."""
    model_config = ConfigDict(from_attributes=True)

    recommendation_id: str = Field(default_factory=lambda: f"rrec_{uuid.uuid4().hex[:8]}")
    title: str
    target_resource: str
    risk_reduction_impact: float = 75.0
    implementation_effort: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    stage: RoadmapStageLiteral = "NOW"
    evidence_references: List[str] = Field(default_factory=list)
    verification_method: str = "DIGITAL_TWIN_RE_SIMULATION"


class ResilienceImprovementRoadmapDTO(BaseModel):
    """Prioritized Resilience Improvement Roadmap (Section 53)."""
    model_config = ConfigDict(from_attributes=True)

    now_actions: List[ResilienceRecommendationDTO] = Field(default_factory=list)
    next_actions: List[ResilienceRecommendationDTO] = Field(default_factory=list)
    later_actions: List[ResilienceRecommendationDTO] = Field(default_factory=list)
    total_actions: int = 0


class CyberResilienceTwinCenterSummaryDTO(BaseModel):
    """Aggregated Dashboard Summary for Cyber Resilience Digital Twin (Section 54)."""
    model_config = ConfigDict(from_attributes=True)

    twin_id: str
    tenant_id: str = "default_tenant"
    overall_resilience_score: float = 87.28
    twin_completeness: float = 88.0
    twin_confidence: float = 91.0
    twin_freshness: float = 96.0
    active_spofs_count: int = 1
    total_dependencies_count: int = 128
    simulated_scenarios_count: int = 14
    prediction_accuracy_precision: float = 0.92
    last_synchronized: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
