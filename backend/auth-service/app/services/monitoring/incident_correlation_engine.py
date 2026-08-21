"""Incident Correlation & Case Automation Engine (Phase 4.0 Part 6 — Sections 75-80).

Aggregates alerts, campaigns, and attack chains into unified Security Incidents,
enforcing case deduplication and uncertainty preservation.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.continuous_intelligence_models import (
    SecurityAlertDTO,
    SecurityIncidentDTO,
    IncidentTypeLiteral,
    IncidentStatusLiteral,
)


class IncidentCorrelationEngine:
    """Correlates security alerts and graph campaigns into managed Security Incident records."""

    def __init__(self):
        self._incidents: Dict[str, SecurityIncidentDTO] = {}
        self._case_to_incident: Dict[str, str] = {}

    def correlate_alert_to_incident(
        self,
        alert: SecurityAlertDTO,
        case_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
    ) -> SecurityIncidentDTO:
        target_case = case_id or alert.case_id

        # Check existing incident for this case (Section 76)
        if target_case and target_case in self._case_to_incident:
            inc_id = self._case_to_incident[target_case]
            incident = self._incidents[inc_id]
            incident.alert_count += 1
            incident.entity_count += len(alert.entity_ids)
            incident.last_seen = datetime.now(timezone.utc).isoformat()
            incident.updated_at = incident.last_seen
            if alert.priority == "CRITICAL":
                incident.priority = "CRITICAL"
            return incident

        # Derive incident type
        inc_type: IncidentTypeLiteral = (
            "PHISHING_INCIDENT" if "domain" in alert.title.lower() or "url" in alert.title.lower()
            else "MALWARE_INCIDENT" if "hash" in alert.title.lower() or "malware" in alert.title.lower()
            else "MULTI_MODAL_INCIDENT"
        )

        incident = SecurityIncidentDTO(
            incident_id=f"inc_{uuid.uuid4().hex[:12]}",
            case_id=target_case,
            incident_type=inc_type,
            title=f"Security Incident: {alert.title}",
            status="DETECTED",
            priority=alert.priority,
            severity=alert.severity,
            confidence=alert.confidence,
            campaign_id=campaign_id or alert.campaign_id,
            attack_chain_id=alert.attack_chain_id,
            alert_count=1,
            entity_count=max(1, len(alert.entity_ids)),
            organization_id=alert.organization_id,
        )

        self._incidents[incident.incident_id] = incident
        if target_case:
            self._case_to_incident[target_case] = incident.incident_id

        return incident

    def get_incident(self, incident_id: str) -> Optional[SecurityIncidentDTO]:
        return self._incidents.get(incident_id)

    def list_incidents(self) -> List[SecurityIncidentDTO]:
        return list(self._incidents.values())
