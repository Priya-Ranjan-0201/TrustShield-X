"""
Cyber Digital Twin & Autonomous Defense Pydantic DTO Models (Phase 35)
======================================================================
Defines all domain models for:
- Digital Twin Environments & State
- Immutable Snapshots & Snapshot Diffing
- Environment Dependencies & Business Impact
- Digital Twin Fidelity Dimensions & Fidelity Gaps
- Simulation Scenarios (9 Simulation Modes)
- Multi-Stage Attack Simulations & Adversary Emulation (MITRE ATT&CK)
- Predictive Attack Paths & Reachability Ranking
- Defensive Simulation & What-If Queries
- Control Failure Simulation & Control Gaps
- Defensive Strategy Optimization (Pareto Minimal Actions)
- Autonomous Defense (Autonomy Levels 0 to 4, Allowlist, Protected Targets)
- Dry-Run, Action Preview, Four-Eyes Approvals, Execution
- Post-Action Verification, Automatic Rollback & Action Circuit Breakers
- Incident Replay & Purple-Team Simulation
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import datetime


class DigitalTwinEnvironmentDTO(BaseModel):
    environment_id: str
    tenant_id: str
    version: str = "1.0.0"
    environment_type: str = "PRODUCTION_REPLICA"  # PRODUCTION_REPLICA, STAGING, TEST, SIMULATION, WHAT_IF
    state_hash: str
    asset_count: int = 0
    relationship_count: int = 0
    fidelity_score: float = 0.95
    source_snapshot: Optional[str] = None
    created_at: str
    updated_at: str


class DigitalTwinSnapshotDTO(BaseModel):
    snapshot_id: str
    environment_id: str
    tenant_id: str
    source: str = "SCHEDULED_SYNC"
    state_hash: str
    asset_count: int = 0
    relationship_count: int = 0
    version: str = "1.0.0"
    is_immutable: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str


class DigitalTwinDiffDTO(BaseModel):
    diff_id: str
    tenant_id: str
    base_snapshot_id: str
    target_snapshot_id: str
    new_assets: List[Dict[str, Any]] = Field(default_factory=list)
    removed_assets: List[Dict[str, Any]] = Field(default_factory=list)
    changed_services: List[Dict[str, Any]] = Field(default_factory=list)
    changed_vulnerabilities: List[Dict[str, Any]] = Field(default_factory=list)
    changed_privileges: List[Dict[str, Any]] = Field(default_factory=list)
    changed_controls: List[Dict[str, Any]] = Field(default_factory=list)
    changed_network_paths: List[Dict[str, Any]] = Field(default_factory=list)
    total_delta_count: int = 0
    calculated_at: str


class DigitalTwinFidelityDTO(BaseModel):
    fidelity_id: str
    tenant_id: str
    environment_id: str
    asset_fidelity: float = 0.98
    network_fidelity: float = 0.95
    identity_fidelity: float = 0.96
    vulnerability_fidelity: float = 0.94
    control_fidelity: float = 0.92
    dependency_fidelity: float = 0.90
    overall_fidelity: float = 0.94
    fidelity_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    evaluated_at: str


class SimulationScenarioDTO(BaseModel):
    scenario_id: str
    tenant_id: str
    name: str
    description: str
    creator: str = "SecOps"
    scope: List[str] = Field(default_factory=list)
    initial_state: Dict[str, Any] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    threat: Optional[str] = None
    objective: str
    simulation_mode: str = "WHAT_IF"  # WHAT_IF, ATTACK_SIMULATION, DEFENSE_SIMULATION, CONTROL_FAILURE, DISASTER, INCIDENT_REPLAY, RED_TEAM, BLUE_TEAM, PURPLE_TEAM
    status: str = "DRAFT"  # DRAFT, READY, RUNNING, COMPLETED, FAILED, CANCELLED, REVIEW_REQUIRED
    created_at: str
    updated_at: str


class AttackSimulationStepDTO(BaseModel):
    step_id: str
    action: str
    tactic: str
    technique: str
    sub_technique: Optional[str] = None
    source: str
    target: str
    prerequisite: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)
    probability: float = 0.5
    confidence: float = 0.9
    simulation_state: str = "SIMULATED"


class PredictedAttackPathDTO(BaseModel):
    prediction_id: str
    tenant_id: str
    scenario_id: str
    entry_point: str
    predicted_next_steps: List[str] = Field(default_factory=list)
    reachable_assets: List[str] = Field(default_factory=list)
    privilege_transitions: List[str] = Field(default_factory=list)
    control_bypass_opportunities: List[str] = Field(default_factory=list)
    reachability_rank: float = 0.8
    risk_score: float = 7.5
    is_hypothetical: bool = True
    status: str = "PREDICTED_ATTACK_PATH"
    confidence: float = 0.85


class WhatIfResultDTO(BaseModel):
    what_if_id: str
    tenant_id: str
    query: str
    target: str
    action: str
    current_state_summary: Dict[str, Any]
    simulated_state_summary: Dict[str, Any]
    risk_change: float
    attack_path_change: Dict[str, Any]
    control_change: Dict[str, Any]
    business_impact: str
    confidence: float = 0.95
    evaluated_at: str


class DefenseStrategyDTO(BaseModel):
    strategy_id: str
    tenant_id: str
    name: str
    actions: List[Dict[str, Any]]
    simulated_risk_reduction: float
    attack_paths_removed: int
    attack_paths_remaining: int
    operational_cost: str
    operational_impact: str
    confidence: float = 0.95
    is_pareto_optimal: bool = True


class AutonomousActionDTO(BaseModel):
    action_id: str
    tenant_id: str
    actor: str = "AutonomousDefenseEngine"
    target: str
    action_type: str
    category: str = "REVERSIBLE"  # READ_ONLY, REVERSIBLE, HIGH_IMPACT, DESTRUCTIVE, TENANT_IMPACTING, PRODUCTION_IMPACTING
    severity: str = "MEDIUM"
    risk_score: float = 3.0
    confidence: float = 0.95
    autonomy_level: str = "LEVEL_2"  # LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4
    approval_requirement: str = "HUMAN_APPROVAL_REQUIRED"
    status: str = "SIMULATED"  # SIMULATED, PREVIEW, PENDING_APPROVAL, APPROVED, EXECUTED, VERIFIED, ROLLED_BACK, FAILED
    approval_ids: List[str] = Field(default_factory=list)
    execution_result: Optional[Dict[str, Any]] = None
    verification_status: str = "NOT_VERIFIED"  # VERIFIED, PARTIALLY_VERIFIED, FAILED, NOT_VERIFIED
    rollback_status: Optional[str] = None  # PENDING, ROLLED_BACK, ROLLBACK_FAILED, ROLLBACK_NOT_VERIFIED
    created_at: str
    executed_at: Optional[str] = None
