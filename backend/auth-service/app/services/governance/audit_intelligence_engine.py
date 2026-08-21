"""Audit Intelligence & Governance Anomaly Detection Engine (Phase 4.0 Part 8 — Sections 51-52, 98).

Analyzes audit telemetry to detect privilege escalations, mass exports, and excessive access denials.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.governance_models import (
    AuditEventDTO,
    GovernanceAlertDTO,
    GovernanceAlertTypeLiteral,
)


class AuditIntelligenceEngine:
    """Detects administrative security anomalies and suspicious access patterns."""

    @staticmethod
    def analyze_audit_stream(events: List[AuditEventDTO]) -> List[GovernanceAlertDTO]:
        alerts: List[GovernanceAlertDTO] = []
        denials_by_actor: Dict[str, int] = {}
        exports_by_actor: Dict[str, int] = {}
        role_changes_by_actor: Dict[str, int] = {}

        for e in events:
            # 1. Track Access Denials
            if e.result in ("DENIED", "BLOCKED", "REQUIRE_MFA"):
                denials_by_actor[e.actor_id] = denials_by_actor.get(e.actor_id, 0) + 1

            # 2. Track Data Exports
            if e.action == "export":
                exports_by_actor[e.actor_id] = exports_by_actor.get(e.actor_id, 0) + 1

            # 3. Track Role / Permission Mutations
            if e.action in ("role_change", "permission_change", "policy_change"):
                role_changes_by_actor[e.actor_id] = role_changes_by_actor.get(e.actor_id, 0) + 1

        # Evaluate thresholds
        for actor, count in denials_by_actor.items():
            if count >= 3:
                alerts.append(
                    GovernanceAlertDTO(
                        organization_id=events[0].organization_id if events else "org_default",
                        alert_type="EXCESSIVE_DENIALS",
                        severity="HIGH",
                        title=f"Excessive Authorization Denials for {actor}",
                        description=f"Actor '{actor}' encountered {count} authorization rejections.",
                        actor_id=actor,
                    )
                )

        for actor, count in exports_by_actor.items():
            if count >= 3:
                alerts.append(
                    GovernanceAlertDTO(
                        organization_id=events[0].organization_id if events else "org_default",
                        alert_type="MASS_EXPORT",
                        severity="CRITICAL",
                        title=f"Potential Mass Data Export by {actor}",
                        description=f"Actor '{actor}' initiated {count} data exports in rapid succession.",
                        actor_id=actor,
                    )
                )

        for actor, count in role_changes_by_actor.items():
            if count >= 3:
                alerts.append(
                    GovernanceAlertDTO(
                        organization_id=events[0].organization_id if events else "org_default",
                        alert_type="PRIVILEGE_ESCALATION",
                        severity="CRITICAL",
                        title=f"Unusual Administrative Role Changes by {actor}",
                        description=f"Actor '{actor}' performed {count} privilege modifications.",
                        actor_id=actor,
                    )
                )

        return alerts
