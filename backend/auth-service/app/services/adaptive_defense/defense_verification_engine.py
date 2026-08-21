"""
TruthShield X — Defense Verification Engine (Phase 17).

Empirically verifies post-adaptation security states and flags simulation/production divergence.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.schemas.adaptive_defense_models import (
    DefenseChangeRecordDTO,
    DefenseSimulationResultDTO,
    VerificationOutcomeLiteral,
)


class DefenseVerificationEngine:
    """Validates intended post-adaptation environment state against simulations."""

    def verify_change(
        self,
        change: DefenseChangeRecordDTO,
        actual_observed_state: Dict[str, Any],
        simulation: Optional[DefenseSimulationResultDTO] = None,
    ) -> VerificationOutcomeLiteral:
        """Verifies adaptation outcome against expected policy and simulation."""
        # 1. State verification check (Section 58)
        if actual_observed_state.get("status") != "ACTIVE" and not actual_observed_state.get("is_mitigated"):
            change.verification_status = "VERIFICATION_FAILED"
            change.verified_at = datetime.now(timezone.utc).isoformat()
            return "VERIFICATION_FAILED"

        # 2. Simulation Divergence Check (Section 75)
        if simulation and simulation.simulated_after_state:
            expected_exposure = simulation.simulated_after_state.get("active_threat_exposure", 0.15)
            actual_exposure = actual_observed_state.get("actual_threat_exposure", expected_exposure)

            if abs(actual_exposure - expected_exposure) > 0.30:
                change.verification_status = "SIMULATION_PRODUCTION_DIVERGENCE"
                change.verified_at = datetime.now(timezone.utc).isoformat()
                return "SIMULATION_PRODUCTION_DIVERGENCE"

        change.verification_status = "VERIFIED"
        change.verified_at = datetime.now(timezone.utc).isoformat()
        return "VERIFIED"
