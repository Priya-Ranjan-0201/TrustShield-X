"""
TruthShield X — Phase 18 Digital Twin 2.0 & Cyber Resilience Endpoints.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.cyber_resilience_twin_models import (
    TwinStateSnapshotDTO,
    TwinCompletenessScoreDTO,
    CyberDependencyGraphDTO,
    CyberResilienceScoreDTO,
    ScenarioModelDTO,
    WhatIfQueryDTO,
    WhatIfResultDTO,
    CounterfactualComparisonDTO,
    PredictionAccuracyMetricsDTO,
    ResilienceImprovementRoadmapDTO,
    CyberResilienceTwinCenterSummaryDTO,
)
from app.services.resilience_twin.cyber_resilience_digital_twin import CyberResilienceDigitalTwin

router = APIRouter(tags=["Cyber Resilience Digital Twin & Predictive Simulation"])

_twin = CyberResilienceDigitalTwin()


class CreateScenarioRequest(BaseModel):
    scenario_type: str
    initial_conditions: str = "CURRENT_STATE"
    assumptions: List[str] = []
    affected_assets: List[str] = []
    threat_model: str = "GENERIC_THREAT"
    is_ai_generated: bool = False


class RunSimulationRequest(BaseModel):
    scenario_id: str
    target_resource: str
    simulated_change: str = "CONTROL_BYPASS"


class CancelSimulationRequest(BaseModel):
    reason: str = "Operator cancelled"


# ============================================================================
# Digital Twin State & Snapshots
# ============================================================================

@router.get("/api/v1/digital-twin", response_model=CyberResilienceTwinCenterSummaryDTO)
def get_digital_twin_summary(tenant_id: str = "default_tenant") -> CyberResilienceTwinCenterSummaryDTO:
    """Returns aggregated executive summary of Digital Twin 2.0."""
    return _twin.get_summary(tenant_id)


@router.get("/api/v1/digital-twin/snapshots", response_model=List[TwinStateSnapshotDTO])
def list_twin_snapshots(tenant_id: str = "default_tenant") -> List[TwinStateSnapshotDTO]:
    """Returns historical immutable state snapshots."""
    snaps = _twin.snapshots.list_snapshots(tenant_id)
    if not snaps:
        return [_twin.snapshots.capture_snapshot(tenant_id)]
    return snaps


@router.get("/api/v1/digital-twin/diff")
def get_twin_diff(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Returns state differences between current and previous snapshots."""
    snaps = _twin.snapshots.list_snapshots(tenant_id)
    if not snaps:
        snap = _twin.snapshots.capture_snapshot(tenant_id)
        return _twin.diff.compare_snapshots(None, snap)

    curr = snaps[-1]
    prev = snaps[-2] if len(snaps) >= 2 else None
    return _twin.diff.compare_snapshots(prev, curr)


@router.get("/api/v1/digital-twin/dependencies", response_model=CyberDependencyGraphDTO)
def get_cyber_dependencies() -> CyberDependencyGraphDTO:
    """Returns topological dependency graph."""
    return _twin.dependencies.build_graph()


@router.get("/api/v1/digital-twin/resilience", response_model=CyberResilienceScoreDTO)
def get_resilience_score(tenant_id: str = "default_tenant") -> CyberResilienceScoreDTO:
    """Returns 7-dimensional cyber resilience scorecard."""
    return _twin.resilience.calculate_resilience(tenant_id)


# ============================================================================
# Scenarios & Simulations
# ============================================================================

@router.get("/api/v1/scenarios", response_model=List[ScenarioModelDTO])
def list_scenarios() -> List[ScenarioModelDTO]:
    """Returns catalog of versioned simulation scenarios."""
    return _twin.scenarios.list_scenarios()


@router.post("/api/v1/scenarios", response_model=ScenarioModelDTO)
def create_scenario(payload: CreateScenarioRequest) -> ScenarioModelDTO:
    """Registers a new scenario."""
    return _twin.scenarios.register_scenario(
        scenario_type=payload.scenario_type,
        initial_conditions=payload.initial_conditions,  # type: ignore
        assumptions=payload.assumptions,
        affected_assets=payload.affected_assets,
        threat_model=payload.threat_model,
        is_ai_generated=payload.is_ai_generated,
    )


@router.get("/api/v1/simulations")
def list_simulations() -> List[Dict[str, Any]]:
    """Lists recent simulations."""
    return [{"simulation_id": "sim_sample_01", "status": "COMPLETED", "label": "SIMULATED"}]


@router.post("/api/v1/simulations", response_model=WhatIfResultDTO)
def run_simulation(payload: RunSimulationRequest) -> WhatIfResultDTO:
    """Executes a what-if simulation against the digital twin sandbox."""
    _twin.sandbox.validate_simulation_request(node_count=10)
    query = WhatIfQueryDTO(
        target_resource=payload.target_resource,
        simulated_change=payload.simulated_change,
    )
    return _twin.what_if.simulate_what_if(query)


@router.get("/api/v1/simulations/{simulation_id}")
def get_simulation(simulation_id: str) -> Dict[str, Any]:
    """Returns details for a simulation run."""
    return {
        "simulation_id": simulation_id,
        "status": "COMPLETED",
        "label": "SIMULATED",
        "is_cancelled": _twin.sandbox.is_cancelled(simulation_id),
    }


@router.post("/api/v1/simulations/{simulation_id}/cancel")
def cancel_simulation(simulation_id: str, payload: Optional[CancelSimulationRequest] = None) -> Dict[str, Any]:
    """Cancels an active simulation."""
    reason = payload.reason if payload else "Operator cancelled"
    _twin.sandbox.cancel_simulation(simulation_id, reason)
    return {"simulation_id": simulation_id, "status": "CANCELLED", "reason": reason}


@router.get("/api/v1/simulations/{simulation_id}/compare", response_model=CounterfactualComparisonDTO)
def compare_simulation(simulation_id: str) -> CounterfactualComparisonDTO:
    """Returns counterfactual comparison across defense strategies."""
    return _twin.counterfactual.compare_scenarios()


# ============================================================================
# Resilience Recommendations & Roadmap
# ============================================================================

@router.get("/api/v1/resilience/roadmap", response_model=ResilienceImprovementRoadmapDTO)
def get_resilience_roadmap() -> ResilienceImprovementRoadmapDTO:
    """Returns prioritized NOW / NEXT / LATER roadmap."""
    return _twin.roadmap.generate_roadmap()


@router.get("/api/v1/resilience/accuracy", response_model=PredictionAccuracyMetricsDTO)
def get_prediction_accuracy() -> PredictionAccuracyMetricsDTO:
    """Returns statistical prediction accuracy and calibration metrics."""
    return _twin.comparator.get_accuracy_metrics()
