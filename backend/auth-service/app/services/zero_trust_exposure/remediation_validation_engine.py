"""
Remediation Validation & Prioritization Engine (Phase 34)
=========================================================
Prioritizes remediation actions based on reachability, exploitability, and business impact.
Enforces mandatory independent rescan verification (REMEDIATION_NOT_VERIFIED without proof).
"""

from typing import Dict, Any, List, Optional
import datetime
from app.schemas.zero_trust_exposure_models import RemediationActionDTO


class RemediationValidationEngine:
    VALID_ACTIONS = [
        "PATCH", "CONFIGURE", "RESTRICT_ACCESS", "REMOVE_EXPOSURE",
        "ROTATE_CREDENTIAL", "SEGMENT", "DISABLE_SERVICE", "MONITOR", "INVESTIGATE"
    ]

    def __init__(self):
        self._actions: Dict[str, Dict[str, Any]] = {}

    def create_remediation_plan(
        self,
        action_id: str,
        tenant_id: str,
        exposure_id: str,
        recommendation_type: str,
        title: str,
        description: str,
        composite_risk: float = 5.0
    ) -> Dict[str, Any]:
        if recommendation_type not in self.VALID_ACTIONS:
            recommendation_type = "RESTRICT_ACCESS"

        priority = "CRITICAL" if composite_risk >= 8.5 else "HIGH" if composite_risk >= 6.0 else "MEDIUM"

        action = {
            "action_id": action_id,
            "tenant_id": tenant_id,
            "exposure_id": exposure_id,
            "recommendation_type": recommendation_type,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "PENDING",
            "validation_status": "REMEDIATION_NOT_VERIFIED",
            "evidence": None,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._actions[action_id] = action
        return action

    def verify_remediation(
        self,
        action_id: str,
        tenant_id: str,
        rescan_telemetry: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        action = self._actions.get(action_id)
        if not action or action["tenant_id"] != tenant_id:
            return {"status": "FAILED", "reason": "ACTION_NOT_FOUND"}

        # Invariant: Never assume remediation succeeded without independent validation
        if not rescan_telemetry or not rescan_telemetry.get("independent_scan_passed", False):
            action["validation_status"] = "REMEDIATION_NOT_VERIFIED"
            action["status"] = "VALIDATION_REQUIRED"
            return {
                "action_id": action_id,
                "validation_status": "REMEDIATION_NOT_VERIFIED",
                "message": "Independent verification scan required to confirm exposure closure"
            }

        action["validation_status"] = "CONFIRMED_REMEDIATED"
        action["status"] = "VERIFIED"
        action["evidence"] = rescan_telemetry
        return {
            "action_id": action_id,
            "validation_status": "CONFIRMED_REMEDIATED",
            "status": "VERIFIED",
            "evidence": rescan_telemetry
        }

    def get_actions(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [a for a in self._actions.values() if a["tenant_id"] == tenant_id]


remediation_validation_engine = RemediationValidationEngine()
