"""
TruthShield X — Action Verification Engine (Phase 30).

Validates post-action outcomes using actual telemetry rather than assumptions or model predictions.
"""

from typing import Dict, List, Optional
from app.schemas.autonomous_defense_models import ActionVerificationDTO


class ActionVerificationEngine:
    """Verifies that automated or human actions accomplished their intended state without adverse side-effects."""

    def __init__(self):
        self._verifications: Dict[str, ActionVerificationDTO] = {}

    def verify_action(
        self,
        action_id: str,
        target: str,
        intended_outcome: str,
        observed_outcome: str,
        telemetry_matches: bool,
    ) -> ActionVerificationDTO:
        dto = ActionVerificationDTO(
            action_id=action_id,
            target=target,
            intended_outcome=intended_outcome,
            observed_outcome=observed_outcome,
            is_verified=telemetry_matches,
            verification_status="VERIFIED" if telemetry_matches else "OUTCOME_NOT_VERIFIED",
        )
        self._verifications[action_id] = dto
        return dto

    def get_verification(self, action_id: str) -> Optional[ActionVerificationDTO]:
        return self._verifications.get(action_id)
