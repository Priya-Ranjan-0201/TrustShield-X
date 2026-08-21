"""Incident Timeline & SLA Tracking Engines (Phase 4.0 Part 7 — Sections 22-26).

Provides an immutable chronological audit trail for incidents and computes SLA deadlines.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone, timedelta
from app.schemas.soc_operations_models import (
    IncidentTimelineEventDTO,
    IncidentSLADTO,
    SecurityIncidentDTO,
    TimelineEventTypeLiteral,
    SLAStatusLiteral,
)


class IncidentTimelineEngine:
    """Manages chronological timeline events for incident auditability."""

    def __init__(self):
        self._timeline: Dict[str, List[IncidentTimelineEventDTO]] = {}

    def add_event(
        self,
        incident_id: str,
        event_type: TimelineEventTypeLiteral,
        description: str,
        actor: str = "SYSTEM",
        source: str = "SOC_AUTOMATION",
        entity_ids: Optional[List[str]] = None,
        evidence_ids: Optional[List[str]] = None,
        alert_id: Optional[str] = None,
        action_id: Optional[str] = None,
    ) -> IncidentTimelineEventDTO:
        event = IncidentTimelineEventDTO(
            timeline_event_id=f"tle_{uuid.uuid4().hex[:12]}",
            incident_id=incident_id,
            event_type=event_type,
            source=source,
            actor=actor,
            description=description,
            entity_ids=entity_ids or [],
            evidence_ids=evidence_ids or [],
            alert_id=alert_id,
            action_id=action_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        if incident_id not in self._timeline:
            self._timeline[incident_id] = []
        self._timeline[incident_id].append(event)
        return event

    def get_timeline(self, incident_id: str) -> List[IncidentTimelineEventDTO]:
        return self._timeline.get(incident_id, [])


class SLAEngine:
    """Computes and tracks incident resolution SLAs based on severity and policy."""

    @staticmethod
    def calculate_sla(incident: SecurityIncidentDTO) -> IncidentSLADTO:
        now = datetime.now(timezone.utc)
        sev = incident.severity

        # SLA thresholds by severity (ack, triage, containment, resolution) in minutes
        sla_matrix = {
            "CRITICAL": (15, 30, 120, 240),
            "HIGH": (30, 60, 240, 480),
            "MEDIUM": (60, 120, 480, 1440),
            "LOW": (120, 240, 1440, 2880),
            "INFORMATIONAL": (240, 480, 2880, 5760),
        }

        ack_m, tri_m, con_m, res_m = sla_matrix.get(sev, (60, 120, 480, 1440))

        return IncidentSLADTO(
            sla_id=f"sla_{uuid.uuid4().hex[:12]}",
            incident_id=incident.incident_id,
            ack_deadline=(now + timedelta(minutes=ack_m)).isoformat(),
            triage_deadline=(now + timedelta(minutes=tri_m)).isoformat(),
            containment_deadline=(now + timedelta(minutes=con_m)).isoformat(),
            resolution_deadline=(now + timedelta(minutes=res_m)).isoformat(),
            status="ON_TRACK",
        )

    @staticmethod
    def evaluate_sla_status(sla: IncidentSLADTO) -> SLAStatusLiteral:
        now = datetime.now(timezone.utc)
        res_deadline = datetime.fromisoformat(sla.resolution_deadline)
        if now > res_deadline:
            sla.status = "BREACHED"
            return "BREACHED"
        if (res_deadline - now).total_seconds() < 1800:  # within 30 min of breach
            sla.status = "WARNING"
            return "WARNING"
        return "ON_TRACK"
