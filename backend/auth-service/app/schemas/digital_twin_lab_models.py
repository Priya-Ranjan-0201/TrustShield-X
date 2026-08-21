"""
TruthShield X — Cyber Defense Digital Twin & Simulation Lab Models (Phase 26).

Strictly typed Pydantic models for Digital Twin States, Snapshots, Twin Drift, Security Scenarios,
Attack Paths, Defense Paths, What-If Analyses, Business Impacts, Strategy Comparisons,
Probabilistic Simulations, and Model Calibration Records.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 26)
# ============================================================================

ScenarioCategoryLiteral = Literal[
    "THREAT",
    "ATTACK",
    "CONTROL_FAILURE",
    "SERVICE_FAILURE",
    "DATA_FAILURE",
    "IDENTITY_FAILURE",
    "NETWORK_FAILURE",
    "INFRASTRUCTURE_FAILURE",
    "POLICY_CHANGE",
    "DETECTION_CHANGE",
    "RESPONSE_CHANGE",
    "RECOVERY_CHANGE",
    "CONFIGURATION_CHANGE",
    "THREAT_EVOLUTION",
]

SimulationStatusLiteral = Literal[
    "PLANNED",
    "RUNNING",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
]

ClaimStatusLiteral = Literal[
    "OBSERVED",
    "MODELED",
    "SIMULATED",
    "PREDICTED",
    "CALIBRATED",
    "INCONCLUSIVE",
    "STALE",
    "UNKNOWN",
    "NOT_VERIFIED",
]

DriftCategoryLiteral = Literal[
    "ASSET_DRIFT",
    "DEPENDENCY_DRIFT",
    "CONFIGURATION_DRIFT",
    "SECURITY_CONTROL_DRIFT",
    "THREAT_DRIFT",
    "RECOVERY_DRIFT",
    "IDENTITY_DRIFT",
]

CalibrationErrorLiteral = Literal[
    "UNDERPREDICTION",
    "OVERPREDICTION",
    "CORRECT",
    "INCONCLUSIVE",
]


# ============================================================================
# Digital Twin State & Snapshot Branching Models
# ============================================================================

class DigitalTwinStateDTO(BaseModel):
    state_id: str = Field(default_factory=lambda: f"twstate_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    version: str = "v1.0.0-PROD-SYNC"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    environment: Literal["PRODUCTION_MIRROR", "STAGING_MIRROR", "SYNTHETIC_LAB"] = "PRODUCTION_MIRROR"
    assets: List[Dict[str, Any]] = Field(default_factory=list)
    services: List[Dict[str, Any]] = Field(default_factory=list)
    identities: List[Dict[str, Any]] = Field(default_factory=list)
    dependencies: List[Dict[str, Any]] = Field(default_factory=list)
    controls: List[Dict[str, Any]] = Field(default_factory=list)
    vulnerabilities: List[Dict[str, Any]] = Field(default_factory=list)
    threats: List[Dict[str, Any]] = Field(default_factory=list)
    detections: List[Dict[str, Any]] = Field(default_factory=list)
    playbooks: List[Dict[str, Any]] = Field(default_factory=list)
    recovery_paths: List[Dict[str, Any]] = Field(default_factory=list)
    configurations: Dict[str, Any] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    freshness_status: Literal["FRESH", "STALE_TWIN_STATE"] = "FRESH"
    confidence_score: float = 0.98

    model_config = ConfigDict(frozen=True)


class TwinSnapshotBranchDTO(BaseModel):
    branch_id: str = Field(default_factory=lambda: f"twbr_{uuid.uuid4().hex[:8]}")
    parent_state_id: str
    branch_name: str = "hypothetical_waf_rule_branch"
    hypothetical_changes: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_active: bool = True

    model_config = ConfigDict(frozen=True)


class TwinDriftRecordDTO(BaseModel):
    drift_id: str = Field(default_factory=lambda: f"twdr_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    drift_category: DriftCategoryLiteral = "CONFIGURATION_DRIFT"
    observed_difference: str = "Live API gateway rate-limit threshold differs from Digital Twin model."
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "MEDIUM"
    synchronized_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_reconciled: bool = False

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Security Scenario & Attack/Defense Path Models
# ============================================================================

class SecurityScenarioDTO(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"scen_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    name: str = "Phishing Credential Stuffing & Lateral Movement Drill"
    category: ScenarioCategoryLiteral = "ATTACK"
    objective: str = "Model blast radius and detection efficacy during compromised credential propagation."
    initial_state_version: str = "v1.0.0-PROD-SYNC"
    assumptions: List[str] = Field(default_factory=lambda: ["Attacker holds valid low-privilege employee credentials", "WAF is active"])
    inputs: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=lambda: {"max_lateral_hops": 3, "max_graph_nodes": 50})
    expected_outputs: List[str] = Field(default_factory=lambda: ["containment_time_seconds", "affected_assets_count"])
    safety_classification: Literal["SANDBOX_ISOLATED", "READ_ONLY_SIMULATION"] = "SANDBOX_ISOLATED"
    status: Literal["READY", "SIMULATING", "COMPLETED", "FAILED"] = "READY"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class AttackPathSimulationDTO(BaseModel):
    simulation_id: str = Field(default_factory=lambda: f"atkpath_{uuid.uuid4().hex[:8]}")
    scenario_id: str
    stages: List[Dict[str, Any]] = Field(default_factory=list)
    affected_nodes: List[str] = Field(default_factory=list)
    potential_attack_paths: List[List[str]] = Field(default_factory=list)
    preventive_controls: List[str] = Field(default_factory=list)
    detection_controls: List[str] = Field(default_factory=list)
    response_controls: List[str] = Field(default_factory=list)
    recovery_controls: List[str] = Field(default_factory=list)
    claim_status: ClaimStatusLiteral = "SIMULATED"
    simulated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Business Impact & Strategy Comparison Models
# ============================================================================

class BusinessImpactSimulationDTO(BaseModel):
    impact_id: str = Field(default_factory=lambda: f"bimp_{uuid.uuid4().hex[:8]}")
    scenario_id: str
    affected_services: List[str] = Field(default_factory=list)
    affected_users: int = 150
    service_downtime_minutes: float = 4.5
    data_availability_score: float = 0.99
    operational_impact_score: float = 0.15
    recovery_effort_hours: float = 1.0
    cascade_failures: List[str] = Field(default_factory=list)
    financial_impact_status: Literal["FINANCIAL_IMPACT_NOT_MODELED", "FINANCIAL_IMPACT_ESTIMATED"] = "FINANCIAL_IMPACT_NOT_MODELED"
    claim_status: ClaimStatusLiteral = "MODELED"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class DefenseStrategyComparisonDTO(BaseModel):
    comparison_id: str = Field(default_factory=lambda: f"stratcmp_{uuid.uuid4().hex[:8]}")
    scenario_id: str
    strategies: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    pareto_frontier: List[str] = Field(default_factory=list)
    ranked_strategies: List[str] = Field(default_factory=list)
    recommended_strategy: str = "STRATEGY_A_AUTOMATED_ISOLATION"
    uncertainty_score: float = 0.05
    reversibility: Literal["FULLY_REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE"] = "FULLY_REVERSIBLE"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Calibration & Probabilistic Simulation Models
# ============================================================================

class SimulationCalibrationRecordDTO(BaseModel):
    calibration_id: str = Field(default_factory=lambda: f"calib_{uuid.uuid4().hex[:8]}")
    scenario_id: str
    predicted_outcome: Dict[str, Any] = Field(default_factory=dict)
    actual_outcome: Dict[str, Any] = Field(default_factory=dict)
    error_classification: CalibrationErrorLiteral = "CORRECT"
    bias_metric: float = 0.02
    calibration_score: float = 0.96
    calibrated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
