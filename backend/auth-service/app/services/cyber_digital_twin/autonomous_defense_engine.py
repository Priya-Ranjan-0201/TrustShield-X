"""
Autonomous Cyber Defense Engine (Phase 35)
==========================================
Governs autonomous defensive actions under strict multi-tiered safety constraints:
- Autonomy Levels: LEVEL_0 (Observe), LEVEL_1 (Recommend), LEVEL_2 (Human Approval),
  LEVEL_3 (Limited Autonomy), LEVEL_4 (Governed Autonomy).
- Action Allowlist & Protected Targets Safeguards (Production DBs, IAM Roots, Audit Storage).
- Dry-run Simulation & Action Previews.
- Mandatory Four-Eyes Dual Approval for high-impact/destructive operations.
"""

from typing import Dict, Any, List, Optional
import datetime
import uuid


class AutonomousDefenseEngine:
    AUTONOMY_LEVELS = {
        "LEVEL_0": "OBSERVE_ONLY",
        "LEVEL_1": "RECOMMEND",
        "LEVEL_2": "HUMAN_APPROVAL",
        "LEVEL_3": "LIMITED_AUTONOMY",
        "LEVEL_4": "GOVERNED_AUTONOMY"
    }

    ACTION_CATEGORIES = {
        "READ_ONLY", "REVERSIBLE", "HIGH_IMPACT",
        "DESTRUCTIVE", "TENANT_IMPACTING", "PRODUCTION_IMPACTING"
    }

    # Protected Targets (Cannot be mutated without explicit dual break-glass approval)
    PROTECTED_TARGET_PATTERNS = [
        "DB-MAIN-CORE-VAULT", "PRODUCTION_ROOT_IAM", "AUDIT_LOG_STORAGE",
        "K8S_CONTROL_PLANE_PROD", "HSM_MASTER_KEYSTORE", "TENANT_BOUNDARY_CONTROLLER"
    ]

    # Explicit Action Allowlist for Autonomous Execution (Level 3/4)
    AUTONOMOUS_ALLOWLIST = {
        "INCREASE_LOG_VERBOSITY", "FLUSH_DNS_CACHE", "REFRESH_DEVICE_POSTURE_PROBE",
        "QUARANTINE_NON_CRITICAL_ENDPOINT", "ROTATE_EPHEMERAL_TOKEN", "BLOCK_SUSPICIOUS_IP_ON_WAF"
    }

    def __init__(self):
        self._actions: Dict[str, Dict[str, Any]] = {}
        self._approvals: Dict[str, List[str]] = {}
        self._tenant_autonomy_level: Dict[str, str] = {}

    def set_tenant_autonomy_level(self, tenant_id: str, level: str) -> Dict[str, Any]:
        lvl = level.upper()
        if lvl not in self.AUTONOMY_LEVELS:
            lvl = "LEVEL_2"
        self._tenant_autonomy_level[tenant_id] = lvl
        return {"tenant_id": tenant_id, "autonomy_level": lvl, "name": self.AUTONOMY_LEVELS[lvl]}

    def get_tenant_autonomy_level(self, tenant_id: str) -> str:
        return self._tenant_autonomy_level.get(tenant_id, "LEVEL_2")

    def propose_defensive_action(
        self,
        action_id: str,
        tenant_id: str,
        target: str,
        action_type: str,
        category: str = "REVERSIBLE",
        severity: str = "MEDIUM",
        risk_score: float = 4.0,
        confidence: float = 0.95,
        reason: str = "Automated response to detected anomaly"
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        current_level = self.get_tenant_autonomy_level(tenant_id)

        is_protected = any(p in target for p in self.PROTECTED_TARGET_PATTERNS)
        is_allowlisted = action_type in self.AUTONOMOUS_ALLOWLIST

        # Determine approval requirement
        if is_protected or category in ["DESTRUCTIVE", "HIGH_IMPACT", "PRODUCTION_IMPACTING"]:
            approval_requirement = "FOUR_EYES_DUAL_APPROVAL_REQUIRED"
        elif current_level in ["LEVEL_0", "LEVEL_1", "LEVEL_2"] or not is_allowlisted:
            approval_requirement = "HUMAN_APPROVAL_REQUIRED"
        else:
            approval_requirement = "AUTONOMOUS_EXECUTION_PERMITTED"

        action = {
            "action_id": action_id,
            "tenant_id": tenant_id,
            "target": target,
            "action_type": action_type,
            "category": category,
            "severity": severity,
            "risk_score": risk_score,
            "confidence": confidence,
            "reason": reason,
            "autonomy_level": current_level,
            "approval_requirement": approval_requirement,
            "status": "SIMULATED",  # Default dry-run state
            "is_protected_target": is_protected,
            "approvers": [],
            "execution_result": None,
            "verification_status": "NOT_VERIFIED",
            "rollback_supported": category in ["REVERSIBLE", "READ_ONLY"],
            "created_at": now
        }
        self._actions[action_id] = action
        return action

    def generate_dry_run_preview(self, action_id: str, tenant_id: str) -> Dict[str, Any]:
        action = self._actions.get(action_id)
        if not action or action["tenant_id"] != tenant_id:
            raise ValueError(f"Action {action_id} not found")

        action["status"] = "PREVIEW"
        return {
            "action_id": action_id,
            "target": action["target"],
            "action_type": action["action_type"],
            "reason": action["reason"],
            "simulated_effect": f"Simulated {action['action_type']} on {action['target']}. Expected risk drop: -4.0",
            "rollback_method": "REVERT_FIREWALL_OR_UNQUARANTINE",
            "approval_requirement": action["approval_requirement"],
            "dry_run_passed": True,
            "status": "PREVIEW"
        }

    def record_approval(
        self,
        action_id: str,
        tenant_id: str,
        approver_id: str,
        justification: str = "Authorized after operational review"
    ) -> Dict[str, Any]:
        action = self._actions.get(action_id)
        if not action or action["tenant_id"] != tenant_id:
            raise ValueError(f"Action {action_id} not found")

        if approver_id in action["approvers"]:
            raise ValueError("Duplicate approval: Same analyst cannot approve twice (Four-Eyes invariant)")

        action["approvers"].append(approver_id)
        
        req = action["approval_requirement"]
        if req == "FOUR_EYES_DUAL_APPROVAL_REQUIRED" and len(action["approvers"]) >= 2:
            action["status"] = "APPROVED"
        elif req == "HUMAN_APPROVAL_REQUIRED" and len(action["approvers"]) >= 1:
            action["status"] = "APPROVED"

        return {
            "action_id": action_id,
            "approvers": action["approvers"],
            "status": action["status"],
            "approved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def execute_action(
        self,
        action_id: str,
        tenant_id: str,
        executor_id: str = "AutonomousExecutionEngine"
    ) -> Dict[str, Any]:
        action = self._actions.get(action_id)
        if not action or action["tenant_id"] != tenant_id:
            raise ValueError(f"Action {action_id} not found")

        # Safety Check: Block if approval is still required
        if action["approval_requirement"] != "AUTONOMOUS_EXECUTION_PERMITTED" and action["status"] != "APPROVED":
            action["status"] = "BLOCKED"
            return {
                "action_id": action_id,
                "status": "BLOCKED",
                "reason": "MANDATORY_APPROVAL_NOT_SATISFIED"
            }

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        exec_result = {
            "executor": executor_id,
            "executed_at": now,
            "target": action["target"],
            "operation": action["action_type"],
            "success": True,
            "system_response": "Action executed successfully on target"
        }
        action["status"] = "EXECUTED"
        action["execution_result"] = exec_result
        action["executed_at"] = now
        return action

    def get_action(self, action_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        act = self._actions.get(action_id)
        if act and act["tenant_id"] == tenant_id:
            return act
        return None


autonomous_defense_engine = AutonomousDefenseEngine()
