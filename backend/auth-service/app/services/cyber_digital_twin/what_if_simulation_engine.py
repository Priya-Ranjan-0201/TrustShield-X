"""
What-If Security Simulation & Control Gap Engine (Phase 35)
===========================================================
Answers "what-if" security questions non-destructively:
- What if a vulnerability is patched?
- What if a device is isolated or account disabled?
- What if a control fails (Firewall, MFA, EDR, IAM, SIEM, SOAR)?
- Generates CONTROL_GAP findings when attack paths have no effective control.
"""

from typing import Dict, Any, List, Optional
import datetime
import uuid


class WhatIfSimulationEngine:
    VALID_ACTIONS = {
        "PATCH_VULNERABILITY", "ISOLATE_DEVICE", "DISABLE_ACCOUNT",
        "ENABLE_MFA", "REMOVE_SERVICE", "BLOCK_NETWORK_PATH",
        "SIMULATE_CONTROL_FAILURE", "ADD_MICROSEGMENTATION"
    }

    def __init__(self):
        self._simulations: Dict[str, Dict[str, Any]] = {}
        self._control_gaps: List[Dict[str, Any]] = []

    def run_what_if(
        self,
        what_if_id: str,
        tenant_id: str,
        target: str,
        action: str,
        baseline_risk: float = 8.5,
        baseline_attack_paths_count: int = 5
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if action == "PATCH_VULNERABILITY":
            risk_change = -4.5
            paths_removed = 3
            business_impact = "LOW (Rolling patch with zero downtime)"
            control_change = {"action": "VULNERABILITY_REMEDIATED", "target": target}
        elif action == "ISOLATE_DEVICE":
            risk_change = -6.0
            paths_removed = 4
            business_impact = "MEDIUM (Endpoint isolated from network; user offline)"
            control_change = {"action": "DEVICE_QUARANTINED", "target": target}
        elif action == "ENABLE_MFA":
            risk_change = -5.0
            paths_removed = 4
            business_impact = "LOW (Users prompted for FIDO2/TOTP)"
            control_change = {"action": "MFA_ENFORCED", "target": target}
        elif action == "SIMULATE_CONTROL_FAILURE":
            risk_change = +3.5
            paths_removed = 0
            business_impact = "HIGH (Control down; attack surface expanded)"
            control_change = {"action": "CONTROL_DEGRADED", "target": target}
        elif action == "ADD_MICROSEGMENTATION":
            risk_change = -5.5
            paths_removed = 4
            business_impact = "LOW (Zero-trust east-west policy enforced)"
            control_change = {"action": "MICROSEGMENT_ENFORCED", "target": target}
        else:
            risk_change = -2.0
            paths_removed = 1
            business_impact = "LOW"
            control_change = {"action": action, "target": target}

        simulated_risk = max(0.5, min(10.0, baseline_risk + risk_change))
        remaining_paths = max(0, baseline_attack_paths_count - paths_removed)

        result = {
            "what_if_id": what_if_id,
            "tenant_id": tenant_id,
            "query": f"What if we execute {action} on {target}?",
            "target": target,
            "action": action,
            "current_state_summary": {
                "risk_score": baseline_risk,
                "active_attack_paths": baseline_attack_paths_count
            },
            "simulated_state_summary": {
                "risk_score": simulated_risk,
                "active_attack_paths": remaining_paths
            },
            "risk_change": risk_change,
            "attack_path_change": {
                "paths_removed": paths_removed,
                "paths_remaining": remaining_paths
            },
            "control_change": control_change,
            "business_impact": business_impact,
            "confidence": 0.95,
            "is_simulation": True,
            "evaluated_at": now
        }
        self._simulations[what_if_id] = result
        return result

    def detect_control_gaps(
        self,
        tenant_id: str,
        asset_id: str,
        active_controls: List[str]
    ) -> List[Dict[str, Any]]:
        gaps = []
        if "MFA" not in active_controls:
            gaps.append({
                "gap_id": f"GAP-MFA-{uuid.uuid4().hex[:6]}",
                "tenant_id": tenant_id,
                "asset_id": asset_id,
                "finding": "CONTROL_GAP",
                "missing_control": "MFA",
                "severity": "HIGH",
                "recommendation": "Enforce hardware FIDO2 or TOTP"
            })
        if "EDR" not in active_controls:
            gaps.append({
                "gap_id": f"GAP-EDR-{uuid.uuid4().hex[:6]}",
                "tenant_id": tenant_id,
                "asset_id": asset_id,
                "finding": "CONTROL_GAP",
                "missing_control": "EDR",
                "severity": "CRITICAL",
                "recommendation": "Deploy host EDR sensor"
            })
        if "MICROSEGMENTATION" not in active_controls:
            gaps.append({
                "gap_id": f"GAP-SEG-{uuid.uuid4().hex[:6]}",
                "tenant_id": tenant_id,
                "asset_id": asset_id,
                "finding": "CONTROL_GAP",
                "missing_control": "MICROSEGMENTATION",
                "severity": "HIGH",
                "recommendation": "Enforce default-deny east-west trust zone"
            })
        self._control_gaps.extend(gaps)
        return gaps

    def get_control_gaps(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [g for g in self._control_gaps if g["tenant_id"] == tenant_id]


what_if_simulation_engine = WhatIfSimulationEngine()
