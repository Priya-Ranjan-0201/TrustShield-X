"""Incident Triage & Safety Engine (Phase 4.0 Part 7 — Sections 17-19).

Evaluates incident severity, affected blast radius, confidence, uncertainties, and generates
actionable recommendations while strictly prohibiting unapproved automatic destruction.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    SecurityIncidentDTO,
    TriageResultDTO,
    SOCAlertDTO,
    ActionTypeLiteral,
)


class IncidentTriageEngine:
    """Evaluates security incidents and produces comprehensive TriageResult."""

    @staticmethod
    def triage_incident(
        incident: SecurityIncidentDTO,
        associated_alerts: List[SOCAlertDTO],
        is_conflicted_evidence: bool = False,
    ) -> TriageResultDTO:
        # 1. Aggregate entities, evidence, and findings
        all_entities = list(set([e for a in associated_alerts for e in a.entity_ids]))
        all_evidence = list(set([ev for a in associated_alerts for ev in a.evidence_ids]))
        all_findings = list(set([f for a in associated_alerts for f in a.finding_ids]))

        # 2. Identify uncertainties and limitations (Section 17, Mandatory Tests 22, 23, 24)
        uncertainties: List[str] = []
        limitations: List[str] = []

        if not all_evidence:
            uncertainties.append("Missing primary evidence items; evaluation relies on secondary telemetry.")
        if is_conflicted_evidence:
            uncertainties.append("Conflicting threat intelligence received from multiple intelligence sources.")
        if incident.confidence in ("LOW", "PROBABILISTIC"):
            uncertainties.append("Confidence is probabilistic; human analyst verification strongly advised.")

        # 3. Formulate Recommended Actions (Section 17, 19, Mandatory Test 1)
        recommended_actions: List[Dict[str, Any]] = []

        if incident.incident_type == "PHISHING_INCIDENT":
            recommended_actions.append({
                "action_type": "BLOCK_DOMAIN",
                "target": all_entities[0] if all_entities else "suspicious-domain.com",
                "risk": "HIGH",
                "reason": "Phishing credential theft domain active in wild",
                "requires_approval": True,
            })
            recommended_actions.append({
                "action_type": "NOTIFY_USER",
                "target": "affected-users",
                "risk": "LOW",
                "reason": "Alert potentially targeted users",
                "requires_approval": False,
            })
        elif incident.incident_type == "MALWARE_INCIDENT":
            recommended_actions.append({
                "action_type": "QUARANTINE_FILE",
                "target": all_entities[0] if all_entities else "malicious.apk",
                "risk": "HIGH",
                "reason": "Malicious payload detected with high confidence",
                "requires_approval": True,
            })
            recommended_actions.append({
                "action_type": "ISOLATE_DEVICE",
                "target": "endpoint-device-01",
                "risk": "CRITICAL",
                "reason": "Prevent lateral network movement",
                "requires_approval": True,
            })
        elif incident.incident_type == "VOICE_SCAM_INCIDENT":
            recommended_actions.append({
                "action_type": "NOTIFY_ANALYST",
                "target": "fraud-investigation-team",
                "risk": "LOW",
                "reason": "Voice clone fraud pattern detected",
                "requires_approval": False,
            })
        else:
            recommended_actions.append({
                "action_type": "COLLECT_EVIDENCE",
                "target": "case-telemetry",
                "risk": "LOW",
                "reason": "Collect deeper forensic telemetry",
                "requires_approval": False,
            })

        summary = (
            f"Triage complete for {incident.incident_number}. "
            f"Classified as {incident.incident_type} affecting {len(all_entities)} entities. "
            f"{'Immediate human review recommended.' if incident.severity == 'CRITICAL' else 'Standard triage queue.'}"
        )

        return TriageResultDTO(
            triage_id=f"trg_{uuid.uuid4().hex[:12]}",
            incident_id=incident.incident_id,
            classification=incident.incident_type,
            severity=incident.severity,
            priority=incident.priority,
            confidence=incident.confidence,
            summary=summary,
            affected_entities=all_entities,
            evidence_ids=all_evidence,
            finding_ids=all_findings,
            recommended_actions=recommended_actions,
            uncertainties=uncertainties,
            limitations=limitations,
        )
