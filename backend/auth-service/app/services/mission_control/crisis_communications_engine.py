"""
TruthShield X — Crisis Communications Engine

Manages stakeholder notifications with confirmation-level distinction.
Never automatically communicates unverified attribution or fabricated impact.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.mission_control_models import (
    CrisisCommunicationDTO,
    IncidentCommandDTO,
)


STAKEHOLDER_MATRIX = {
    "CRISIS": {
        "channels": ["INTERNAL", "SECURITY_TEAM", "EXECUTIVE", "SERVICE_OWNER", "GOVERNANCE"],
        "priority": "CRITICAL",
    },
    "CRITICAL": {
        "channels": ["INTERNAL", "SECURITY_TEAM", "EXECUTIVE", "SERVICE_OWNER"],
        "priority": "HIGH",
    },
    "HIGH": {
        "channels": ["INTERNAL", "SECURITY_TEAM", "SERVICE_OWNER"],
        "priority": "MEDIUM",
    },
    "MEDIUM": {
        "channels": ["INTERNAL", "SECURITY_TEAM"],
        "priority": "MEDIUM",
    },
    "LOW": {
        "channels": ["INTERNAL"],
        "priority": "LOW",
    },
    "INFORMATIONAL": {
        "channels": ["INTERNAL"],
        "priority": "LOW",
    },
}


class CrisisCommunicationsEngine:
    """Generates and tracks crisis communications with evidence references."""

    def __init__(self):
        self._communications: Dict[str, List[CrisisCommunicationDTO]] = {}

    def generate_notifications(
        self,
        command: IncidentCommandDTO,
        subject: str,
        body: str,
        confirmation_level: str = "UNKNOWN",
        evidence_references: Optional[List[str]] = None,
        sent_by: str = "SYSTEM",
    ) -> List[CrisisCommunicationDTO]:
        """Generates notifications to appropriate stakeholders based on severity."""
        matrix = STAKEHOLDER_MATRIX.get(command.severity, STAKEHOLDER_MATRIX["INFORMATIONAL"])
        channels = matrix["channels"]

        notifications: List[CrisisCommunicationDTO] = []
        for channel in channels:
            comm = CrisisCommunicationDTO(
                incident_command_id=command.incident_command_id,
                channel=channel,
                confirmation_level=confirmation_level,
                subject=subject,
                body=body,
                evidence_references=evidence_references or [],
                sent_by=sent_by,
            )
            notifications.append(comm)

        if command.incident_command_id not in self._communications:
            self._communications[command.incident_command_id] = []
        self._communications[command.incident_command_id].extend(notifications)

        return notifications

    def list_communications(self, command_id: str) -> List[CrisisCommunicationDTO]:
        """Lists all communications for an incident command."""
        return self._communications.get(command_id, [])
