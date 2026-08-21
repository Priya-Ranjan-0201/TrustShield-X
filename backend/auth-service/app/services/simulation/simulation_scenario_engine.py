"""
TruthShield X — Simulation Scenario Execution Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.simulation_models import (
    SimulationRunDTO,
    SimulationScenarioDTO,
    ResponseStrategyComparisonDTO,
    ScenarioTypeLiteral,
)
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService
from app.services.simulation.environment_execution_guard import EnvironmentExecutionGuard


class SimulationScenarioEngine:
    """Executes controlled, non-destructive threat simulations against a Digital Security Twin."""

    def __init__(
        self,
        twin_service: Optional[DigitalSecurityTwinService] = None,
        guard: Optional[EnvironmentExecutionGuard] = None,
    ):
        self.twin_service = twin_service or DigitalSecurityTwinService()
        self.guard = guard or EnvironmentExecutionGuard()

    def run_scenario(
        self,
        twin_id: str,
        scenario_type: ScenarioTypeLiteral,
        target_asset: str = "AuthGatewayAPI",
        simulated_threat_level: float = 0.85,
    ) -> SimulationRunDTO:
        """Executes a non-destructive simulation against the specified Digital Security Twin."""
        twin = self.twin_service.get_twin(twin_id)
        if not twin:
            raise KeyError(f"Twin '{twin_id}' not found.")

        # Enforce execution guard
        self.guard.validate_simulation_action(
            environment=twin.environment,
            action_name=f"RUN_SCENARIO_{scenario_type}",
            target_payload={"target_asset": target_asset},
        )

        sim_id = f"sim_{uuid.uuid4().hex[:10]}"
        baseline_risk = twin.baseline_risk_score
        simulated_risk = min(99.0, baseline_risk + (simulated_threat_level * 50.0))
        risk_delta = round(simulated_risk - baseline_risk, 2)

        # Transition twin state in sandbox
        self.twin_service.transition_state(
            twin_id=twin_id,
            new_state="SIMULATED_COMPROMISED" if simulated_risk > 70 else "EXPOSED",
            simulated_risk_score=simulated_risk,
        )

        # Simulated attack paths
        attack_paths = [
            {
                "path_id": f"spath_{uuid.uuid4().hex[:6]}",
                "entry_point": "SimulatedPhishingDropper",
                "intermediate_step": "StagingTokenHarvest",
                "target_asset": target_asset,
                "classification": "SIMULATED",
                "simulated_lateral_risk": "MODERATE",
            }
        ]

        # Compared response strategies
        strategies = [
            ResponseStrategyComparisonDTO(
                strategy_id="strat_iso",
                strategy_name="Isolate Target Asset",
                action_type="ISOLATE_ASSET",
                simulated_risk_reduction=35.0,
                simulated_exposure_reduction=40.0,
                simulated_blast_radius="MINIMAL",
                operational_impact="MEDIUM",
                reversibility="HIGH",
                safety_score=0.88,
                confidence=0.92,
                recommendation="Recommended: High risk reduction with reversible isolation switch.",
            ),
            ResponseStrategyComparisonDTO(
                strategy_id="strat_rot",
                strategy_name="Rotate Synthetic Credentials & Invalidate Sessions",
                action_type="ROTATE_SYNTHETIC_CREDENTIALS",
                simulated_risk_reduction=25.0,
                simulated_exposure_reduction=30.0,
                simulated_blast_radius="MINIMAL",
                operational_impact="LOW",
                reversibility="HIGH",
                safety_score=0.95,
                confidence=0.95,
                recommendation="Recommended: Zero operational disruption with immediate token revocation.",
            ),
            ResponseStrategyComparisonDTO(
                strategy_id="strat_blk",
                strategy_name="Block External Indicator on Edge WAF",
                action_type="BLOCK_INDICATOR",
                simulated_risk_reduction=20.0,
                simulated_exposure_reduction=20.0,
                simulated_blast_radius="MINIMAL",
                operational_impact="LOW",
                reversibility="HIGH",
                safety_score=0.90,
                confidence=0.90,
                recommendation="Recommended: Blocks inbound traffic from dropper IP/Domain.",
            ),
        ]

        return SimulationRunDTO(
            simulation_id=sim_id,
            twin_id=twin_id,
            scenario_id=f"scen_{scenario_type.lower()}",
            status="COMPLETED",
            baseline_risk=baseline_risk,
            simulated_risk=simulated_risk,
            risk_delta=risk_delta,
            baseline_exposure=25.0,
            simulated_exposure=65.0,
            exposure_delta=40.0,
            simulated_events_count=12,
            simulated_attack_paths=attack_paths,
            compared_strategies=strategies,
            limitations=["Simulation model estimates behavior based on configured control rules; real-world adversary zero-day capabilities may deviate."],
        )
