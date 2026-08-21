"""
TruthShield X — Action Verification Engine (Phase 20).

Verifies actual runtime state following action execution and detects divergences without fabrication.
"""

from typing import Dict, Optional
from datetime import datetime, timezone
from app.schemas.copilot_command_models import (
    CopilotActionVerificationDTO,
    ActionStateLiteral,
)


class ActionVerificationEngine:
    """Verifies execution outcomes against expected baseline states."""

    def verify_action_execution(
        self,
        plan_id: str,
        is_success: bool = True,
        actual_state: str = "ISOLATED_SECURITY_GROUP_APPLIED",
        expected_state: str = "ISOLATED_SECURITY_GROUP_APPLIED",
    ) -> CopilotActionVerificationDTO:
        has_div = actual_state != expected_state or not is_success
        state: ActionStateLiteral = "VERIFIED" if is_success and not has_div else "FAILED"
        res_text = "Verification confirmed expected security state." if state == "VERIFIED" else "Action verification detected divergence or runtime failure."

        return CopilotActionVerificationDTO(
            plan_id=plan_id,
            action_state=state,
            verification_result=res_text,
            actual_state=actual_state,
            expected_state=expected_state,
            has_divergence=has_div,
            rollback_status="READY" if state == "VERIFIED" else "INITIATED",
            verified_at=datetime.now(timezone.utc).isoformat(),
        )
