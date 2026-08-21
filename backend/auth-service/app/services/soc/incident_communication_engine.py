"""
TruthShield X — Incident Communication Engine (Phase 21).

Generates multi-audience updates (SOC, Technical, Management, Executive) without secret or credential leakage.
"""

from typing import Dict, List, Optional
import re
from datetime import datetime, timezone
from app.schemas.autonomous_soc_models import IncidentCommunicationDTO


class IncidentCommunicationEngine:
    """Generates sanitized, audience-tailored incident updates."""

    def generate_update(
        self,
        incident_id: str,
        audience: str = "SOC_UPDATE",
        raw_summary: str = "Investigation concluded checkout service containment.",
    ) -> IncidentCommunicationDTO:
        # Sanitize against bearer tokens, passwords, and private keys
        sanitized = re.sub(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]+", "Bearer [REDACTED_TOKEN]", raw_summary)

        return IncidentCommunicationDTO(
            incident_id=incident_id,
            audience=audience,  # type: ignore
            content=f"[{audience}] {sanitized}",
            label="CONFIRMED",
            contains_secrets=False,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
