"""
TruthShield X — Phase 12 Digital Security Twin & Attack Simulation Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.schemas.simulation_models import (
    DigitalSecurityTwinDTO,
    SimulationRunDTO,
    WhatIfResultDTO,
    WhatIfQueryDTO,
    ResponseStrategyComparisonDTO,
    DisasterRecoverySimulationDTO,
    TwinTypeLiteral,
    ScenarioTypeLiteral,
)
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService
from app.services.simulation.simulation_scenario_engine import SimulationScenarioEngine
from app.services.simulation.what_if_engine import WhatIfEngine
from app.services.simulation.response_strategy_simulation_engine import ResponseStrategySimulationEngine
from app.services.simulation.security_control_effectiveness_engine import SecurityControlEffectivenessEngine
from app.services.simulation.disaster_recovery_simulation_engine import DisasterRecoverySimulationEngine


router = APIRouter(prefix="/twins", tags=["Digital Security Twin & Simulation"])

_twin_service = DigitalSecurityTwinService()
_scenario_engine = SimulationScenarioEngine(twin_service=_twin_service)
_what_if_engine = WhatIfEngine()
_strategy_engine = ResponseStrategySimulationEngine()
_control_engine = SecurityControlEffectivenessEngine()
_dr_engine = DisasterRecoverySimulationEngine()


class CreateTwinRequest(BaseModel):
    source_snapshot_id: str
    raw_assets: List[Dict[str, Any]] = []
    twin_type: TwinTypeLiteral = "BASELINE_TWIN"
    tenant_id: str = "default_tenant"


class RunScenarioRequest(BaseModel):
    scenario_type: ScenarioTypeLiteral = "PHISHING_CAMPAIGN"
    target_asset: str = "AuthGatewayAPI"
    simulated_threat_level: float = 0.85


class DisasterRecoveryRequest(BaseModel):
    component: str = "DATABASE"
    failure_type: str = "PRIMARY_NODE_CRASH"


@router.post("", response_model=DigitalSecurityTwinDTO, status_code=status.HTTP_201_CREATED)
def create_digital_twin(payload: CreateTwinRequest) -> DigitalSecurityTwinDTO:
    """Creates a new isolated Digital Security Twin from a sanctioned snapshot with synthetic credentials."""
    return _twin_service.create_twin_from_snapshot(
        source_snapshot_id=payload.source_snapshot_id,
        raw_assets=payload.raw_assets,
        twin_type=payload.twin_type,
        tenant_id=payload.tenant_id,
    )


@router.get("", response_model=List[DigitalSecurityTwinDTO])
def list_digital_twins(tenant_id: str = "default_tenant") -> List[DigitalSecurityTwinDTO]:
    """Lists Digital Security Twins for tenant."""
    return _twin_service.list_twins(tenant_id)


@router.get("/{twin_id}", response_model=DigitalSecurityTwinDTO)
def get_digital_twin(twin_id: str, tenant_id: str = "default_tenant") -> DigitalSecurityTwinDTO:
    """Retrieves a single Digital Security Twin."""
    twin = _twin_service.get_twin(twin_id, tenant_id)
    if not twin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Digital Security Twin not found.")
    return twin


@router.post("/{twin_id}/scenarios/run", response_model=SimulationRunDTO)
def run_simulation_scenario(twin_id: str, payload: RunScenarioRequest) -> SimulationRunDTO:
    """Executes a non-destructive attack simulation against the Digital Security Twin."""
    try:
        return _scenario_engine.run_scenario(
            twin_id=twin_id,
            scenario_type=payload.scenario_type,
            target_asset=payload.target_asset,
            simulated_threat_level=payload.simulated_threat_level,
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Twin not found.")


@router.post("/{twin_id}/what-if", response_model=WhatIfResultDTO)
def evaluate_what_if_query(twin_id: str, payload: WhatIfQueryDTO) -> WhatIfResultDTO:
    """Answers a counterfactual what-if security query by evaluating hypothetical state changes."""
    return _what_if_engine.evaluate_what_if(
        target_twin_id=twin_id,
        question=payload.question,
        hypothetical_changes=payload.hypothetical_changes,
    )


@router.post("/{twin_id}/compare-responses", response_model=List[ResponseStrategyComparisonDTO])
def compare_response_strategies(twin_id: str, incident_context: Dict[str, Any] = {}) -> List[ResponseStrategyComparisonDTO]:
    """Compares candidate response strategies with simulated risk reduction and safety scores."""
    return _strategy_engine.evaluate_strategies(incident_context)


@router.get("/{twin_id}/control-effectiveness")
def get_control_effectiveness(twin_id: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Evaluates security control effectiveness and identifies defensive gaps."""
    twin = _twin_service.get_twin(twin_id, tenant_id)
    if not twin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Twin not found.")
    return _control_engine.evaluate_controls(twin.modeled_controls)


@router.post("/{twin_id}/disaster-recovery/simulate", response_model=DisasterRecoverySimulationDTO)
def simulate_disaster_recovery(twin_id: str, payload: DisasterRecoveryRequest) -> DisasterRecoverySimulationDTO:
    """Simulates component failover and recovery verification in the sandbox."""
    return _dr_engine.simulate_component_failover(
        component=payload.component,
        failure_type=payload.failure_type,
    )
