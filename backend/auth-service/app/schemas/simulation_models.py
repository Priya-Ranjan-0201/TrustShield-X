"""
TruthShield X — Phase 12 Digital Security Twin & Attack Simulation Data Models
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


TwinTypeLiteral = Literal[
    "BASELINE_TWIN",
    "INCIDENT_TWIN",
    "ASSET_TWIN",
    "CAMPAIGN_TWIN",
    "RESPONSE_TWIN",
    "DISASTER_RECOVERY_TWIN",
    "SECURITY_CONTROL_TWIN",
]

TwinStateLiteral = Literal[
    "NORMAL",
    "EXPOSED",
    "DEGRADED",
    "SIMULATED_COMPROMISED",
    "CONTAINED_SIMULATION",
    "RECOVERING_SIMULATION",
    "RECOVERED_SIMULATION",
]

SimulationStatusLiteral = Literal[
    "CREATED",
    "VALIDATING",
    "READY",
    "RUNNING",
    "PAUSED",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
    "EXPIRED",
]

ScenarioTypeLiteral = Literal[
    "PHISHING_CAMPAIGN",
    "MALWARE_CAMPAIGN",
    "IDENTITY_ABUSE",
    "PAYMENT_FRAUD",
    "API_ABUSE",
    "ACCOUNT_TAKEOVER",
    "DATA_EXPOSURE",
    "SUPPLY_CHAIN_EVENT",
    "THIRD_PARTY_FAILURE",
    "INFRASTRUCTURE_COMPROMISE",
    "INSIDER_RISK_SIMULATION",
    "MULTI_MODAL_CAMPAIGN",
    "DISASTER_RECOVERY",
]


class SecurityControlDTO(BaseModel):
    control_id: str
    name: str
    control_type: str  # WAF, MFA, SEGMENTATION, RATE_LIMIT, EDR, RBAC
    state: Literal["ACTIVE", "DEGRADED", "DISABLED", "BYPASSED_SIMULATION"] = "ACTIVE"
    modeled_effectiveness: float = 0.85
    observed_effectiveness: Optional[float] = 0.80
    confidence: float = 0.90


class DigitalSecurityTwinDTO(BaseModel):
    twin_id: str
    tenant_id: str = "default_tenant"
    version: int = 1
    twin_type: TwinTypeLiteral = "BASELINE_TWIN"
    environment: Literal["SIMULATION"] = "SIMULATION"
    state: TwinStateLiteral = "NORMAL"
    source_snapshot_id: str
    modeled_assets: List[Dict[str, Any]] = Field(default_factory=list)
    modeled_controls: List[SecurityControlDTO] = Field(default_factory=list)
    baseline_risk_score: float = 28.0
    simulated_risk_score: float = 28.0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = "security_architect"
    expiration: Optional[str] = None


class SimulationScenarioDTO(BaseModel):
    scenario_id: str
    name: str
    description: str
    scenario_type: ScenarioTypeLiteral
    assumptions: List[str] = Field(default_factory=list)
    threat_inputs: List[Dict[str, Any]] = Field(default_factory=list)
    target_scope: List[str] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    objectives: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    stop_conditions: List[str] = Field(default_factory=list)


class ResponseStrategyComparisonDTO(BaseModel):
    strategy_id: str
    strategy_name: str
    action_type: str  # ISOLATE_ASSET, ROTATE_SYNTHETIC_CREDENTIALS, BLOCK_INDICATOR, INCREASE_MONITORING
    simulated_risk_reduction: float
    simulated_exposure_reduction: float
    simulated_blast_radius: str  # MINIMAL, MODERATE, EXTENSIVE
    operational_impact: str  # LOW, MEDIUM, HIGH
    reversibility: Literal["HIGH", "MEDIUM", "LOW"]
    safety_score: float  # 0.0 - 1.0
    confidence: float
    recommendation: str


class WhatIfQueryDTO(BaseModel):
    question: str
    hypothetical_changes: Dict[str, Any]
    target_twin_id: str


class WhatIfResultDTO(BaseModel):
    query_id: str
    target_twin_id: str
    question: str
    simulated_risk_delta: float
    simulated_exposure_delta: float
    simulated_trust_delta: float
    affected_assets: List[str]
    simulated_blast_radius: str
    findings: List[str]
    is_simulation: bool = True
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DisasterRecoverySimulationDTO(BaseModel):
    dr_id: str
    component_tested: str  # DATABASE, REDIS, WORKER, API_GATEWAY, EVENT_QUEUE
    simulated_failure_type: str
    failover_sequence_steps: List[str]
    simulated_recovery_duration_seconds: int
    data_consistency_preserved: bool
    audit_chain_continuous: bool
    status: Literal["RECOVERED_SIMULATION", "DEGRADED_SIMULATION", "FAILED_SIMULATION"]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SimulationRunDTO(BaseModel):
    simulation_id: str
    twin_id: str
    scenario_id: str
    status: SimulationStatusLiteral = "COMPLETED"
    baseline_risk: float
    simulated_risk: float
    risk_delta: float
    baseline_exposure: float
    simulated_exposure: float
    exposure_delta: float
    simulated_events_count: int
    simulated_attack_paths: List[Dict[str, Any]] = Field(default_factory=list)
    compared_strategies: List[ResponseStrategyComparisonDTO] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
