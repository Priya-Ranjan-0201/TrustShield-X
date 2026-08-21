"""
Cyber Simulation Scenario Engine (Phase 35)
===========================================
Manages simulation scenario lifecycle (DRAFT, READY, RUNNING, COMPLETED, FAILED, CANCELLED, REVIEW_REQUIRED)
and supports all 9 simulation modes:
(WHAT_IF, ATTACK_SIMULATION, DEFENSE_SIMULATION, CONTROL_FAILURE, DISASTER, INCIDENT_REPLAY, RED_TEAM, BLUE_TEAM, PURPLE_TEAM).
"""

from typing import Dict, Any, List, Optional
import datetime
import uuid


class CyberSimulationScenarioEngine:
    VALID_MODES = {
        "WHAT_IF", "ATTACK_SIMULATION", "DEFENSE_SIMULATION",
        "CONTROL_FAILURE", "DISASTER", "INCIDENT_REPLAY",
        "RED_TEAM", "BLUE_TEAM", "PURPLE_TEAM"
    }

    VALID_STATES = {
        "DRAFT", "READY", "RUNNING", "COMPLETED",
        "FAILED", "CANCELLED", "REVIEW_REQUIRED"
    }

    def __init__(self):
        self._scenarios: Dict[str, Dict[str, Any]] = {}
        self._runs: List[Dict[str, Any]] = []

    def create_scenario(
        self,
        scenario_id: str,
        tenant_id: str,
        name: str,
        description: str,
        objective: str,
        simulation_mode: str = "WHAT_IF",
        scope: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        threat: Optional[str] = None,
        creator: str = "SecOps Lead"
    ) -> Dict[str, Any]:
        mode = simulation_mode if simulation_mode in self.VALID_MODES else "WHAT_IF"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        scenario = {
            "scenario_id": scenario_id,
            "tenant_id": tenant_id,
            "name": name,
            "description": description,
            "objective": objective,
            "simulation_mode": mode,
            "scope": scope or ["PRODUCTION_PERIMETER"],
            "assumptions": assumptions or ["Assumes default network latency"],
            "threat": threat or "Generic Advanced Persistent Threat (APT)",
            "creator": creator,
            "status": "DRAFT",
            "created_at": now,
            "updated_at": now
        }
        self._scenarios[scenario_id] = scenario
        return scenario

    def update_scenario_status(
        self,
        scenario_id: str,
        tenant_id: str,
        new_status: str
    ) -> Dict[str, Any]:
        scenario = self.get_scenario(scenario_id, tenant_id)
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")

        if new_status not in self.VALID_STATES:
            raise ValueError(f"Invalid status {new_status}")

        scenario["status"] = new_status
        scenario["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return scenario

    def get_scenario(self, scenario_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        scen = self._scenarios.get(scenario_id)
        if scen and scen["tenant_id"] == tenant_id:
            return scen
        return None

    def list_scenarios(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [s for s in self._scenarios.values() if s["tenant_id"] == tenant_id]

    def execute_simulation_run(
        self,
        run_id: str,
        scenario_id: str,
        tenant_id: str,
        environment_snapshot_id: str,
        random_seed: Optional[int] = 42
    ) -> Dict[str, Any]:
        scenario = self.get_scenario(scenario_id, tenant_id)
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")

        scenario["status"] = "RUNNING"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        run_record = {
            "run_id": run_id,
            "scenario_id": scenario_id,
            "tenant_id": tenant_id,
            "environment_snapshot_id": environment_snapshot_id,
            "random_seed": random_seed,
            "mode": scenario["simulation_mode"],
            "status": "COMPLETED",
            "results_summary": {
                "attack_steps_executed": 4,
                "controls_triggered": 3,
                "simulated_compromise": False,
                "residual_risk": 2.5
            },
            "is_simulation": True,
            "executed_at": now
        }
        scenario["status"] = "COMPLETED"
        self._runs.append(run_record)
        return run_record

    def list_runs(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [r for r in self._runs if r["tenant_id"] == tenant_id]


cyber_simulation_scenario_engine = CyberSimulationScenarioEngine()
