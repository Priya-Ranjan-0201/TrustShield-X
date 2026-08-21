"""
Crisis Escalation & SLA Management Engine (Phase 36)
====================================================
Monitors crisis severity, blast radius expansion, control failures, and SLA thresholds.
Automatically triggers hierarchical escalations and notifies designated executive stakeholders.
"""

from typing import Dict, Any, List, Optional
import datetime


class CrisisEscalationEngine:
    DEFAULT_SLAS = {
        "DETECTION": {"target_minutes": 15, "severity_multiplier": {"SEV_1": 1.0, "SEV_2": 2.0, "SEV_3": 4.0}},
        "ACKNOWLEDGEMENT": {"target_minutes": 5, "severity_multiplier": {"SEV_1": 1.0, "SEV_2": 2.0, "SEV_3": 4.0}},
        "INVESTIGATION": {"target_minutes": 30, "severity_multiplier": {"SEV_1": 1.0, "SEV_2": 2.0, "SEV_3": 4.0}},
        "CONTAINMENT": {"target_minutes": 60, "severity_multiplier": {"SEV_1": 1.0, "SEV_2": 2.0, "SEV_3": 4.0}},
        "RECOVERY": {"target_minutes": 240, "severity_multiplier": {"SEV_1": 1.0, "SEV_2": 2.0, "SEV_3": 4.0}}
    }

    def __init__(self):
        self._escalation_records: Dict[str, List[Dict[str, Any]]] = {}
        self._stakeholders: Dict[str, List[Dict[str, Any]]] = {}

    def evaluate_escalation_triggers(
        self,
        crisis_id: str,
        tenant_id: str,
        severity: str,
        duration_minutes: int,
        blast_radius_asset_count: int,
        control_failures_count: int
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        triggers = []

        if severity == "SEV_1":
            triggers.append("CRITICAL_SEVERITY_SEV_1")
        if duration_minutes > 120 and severity in {"SEV_1", "SEV_2"}:
            triggers.append("PROLONGED_INCIDENT_DURATION")
        if blast_radius_asset_count >= 5:
            triggers.append("WIDESPREAD_ASSET_IMPACT")
        if control_failures_count >= 2:
            triggers.append("MULTIPLE_DEFENSIVE_CONTROL_FAILURES")

        should_escalate = len(triggers) > 0
        target_tier = "EXECUTIVE_CRISIS_BOARD" if severity == "SEV_1" or len(triggers) >= 2 else "SECOPS_MANAGEMENT"

        record = {
            "crisis_id": crisis_id,
            "tenant_id": tenant_id,
            "escalated": should_escalate,
            "escalation_tier": target_tier if should_escalate else "NO_ESCALATION",
            "matched_triggers": triggers,
            "evaluated_at": now
        }
        if crisis_id not in self._escalation_records:
            self._escalation_records[crisis_id] = []
        self._escalation_records[crisis_id].append(record)
        return record

    def check_sla_status(
        self,
        crisis_id: str,
        tenant_id: str,
        sla_stage: str,  # DETECTION, ACKNOWLEDGEMENT, INVESTIGATION, CONTAINMENT, RECOVERY
        elapsed_minutes: int,
        severity: str = "SEV_1"
    ) -> Dict[str, Any]:
        sla_info = self.DEFAULT_SLAS.get(sla_stage, {"target_minutes": 60, "severity_multiplier": {}})
        mult = sla_info.get("severity_multiplier", {}).get(severity, 1.0)
        target = sla_info["target_minutes"] * mult

        is_breached = elapsed_minutes > target
        is_at_risk = (elapsed_minutes / target) >= 0.75 and not is_breached

        return {
            "crisis_id": crisis_id,
            "tenant_id": tenant_id,
            "sla_stage": sla_stage,
            "severity": severity,
            "target_minutes": target,
            "elapsed_minutes": elapsed_minutes,
            "status": "BREACHED" if is_breached else ("AT_RISK" if is_at_risk else "HEALTHY"),
            "breach_time_remaining": max(0, int(target - elapsed_minutes))
        }

    def register_stakeholder(
        self,
        crisis_id: str,
        tenant_id: str,
        name: str,
        role: str,
        channel: str = "IN_APP"
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        entry = {
            "name": name,
            "role": role,
            "channel": channel,
            "notification_status": "REGISTERED",
            "registered_at": now
        }
        if crisis_id not in self._stakeholders:
            self._stakeholders[crisis_id] = []
        self._stakeholders[crisis_id].append(entry)
        return entry

    def get_stakeholders(self, crisis_id: str) -> List[Dict[str, Any]]:
        return self._stakeholders.get(crisis_id, [])


crisis_escalation_engine = CrisisEscalationEngine()
