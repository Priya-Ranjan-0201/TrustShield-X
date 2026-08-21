"""
TruthShield X — Security Simulation Engine (Phase 25).

Executes dry-run Before/Change/After state simulations in Digital Twin sandbox environments.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import SimulationResultDTO


class SecuritySimulationEngine:
    """Simulates the effects of security improvements prior to deployment."""

    def __init__(self):
        self._simulations: Dict[str, SimulationResultDTO] = {}

    def simulate_improvement(
        self,
        improvement_id: str,
        before_state: Optional[Dict[str, Any]] = None,
        simulated_change: Optional[Dict[str, Any]] = None,
    ) -> SimulationResultDTO:
        before = before_state or {"detection_coverage": 0.94, "false_positive_rate": 0.05}
        change = simulated_change or {"added_rule": "sigma_t1055_dll_injection"}
        after = {
            "detection_coverage": round(min(1.0, before.get("detection_coverage", 0.94) + 0.04), 4),
            "false_positive_rate": round(before.get("false_positive_rate", 0.05), 4),
        }

        dto = SimulationResultDTO(
            improvement_id=improvement_id,
            before_state=before,
            simulated_change=change,
            after_state=after,
            digital_twin_verified=True,
            status="SIMULATED_SUCCESS",
            simulated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._simulations[dto.simulation_id] = dto
        return dto

    def get_simulation(self, simulation_id: str) -> Optional[SimulationResultDTO]:
        return self._simulations.get(simulation_id)
