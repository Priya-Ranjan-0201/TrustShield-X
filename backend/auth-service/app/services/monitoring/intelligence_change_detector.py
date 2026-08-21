"""Intelligence Change Detection Engine (Phase 4.0 Part 6 — Sections 16-18).

Detects indicator additions, reclassifications, revocations, and infrastructure changes,
generating typed, provenance-backed IntelligenceChangeEventDTOs.
"""

from typing import List, Dict, Any, Optional, Tuple
import uuid
from datetime import datetime, timezone
from app.schemas.continuous_intelligence_models import (
    IntelligenceObservationDTO,
    IntelligenceChangeEventDTO,
    IntelligenceEventTypeLiteral,
    AlertSeverityLiteral,
)


class IntelligenceChangeDetector:
    """Detects meaningful changes between incoming observations and historical intelligence state."""

    @staticmethod
    def detect_changes(
        current_observations: List[IntelligenceObservationDTO],
        historical_map: Dict[str, IntelligenceObservationDTO],
    ) -> List[IntelligenceChangeEventDTO]:
        """Compare current observations with historical baseline."""
        changes: List[IntelligenceChangeEventDTO] = []

        for obs in current_observations:
            key = f"{obs.indicator_type}:{obs.indicator_value_hash}"
            historical = historical_map.get(key)

            if historical is None:
                # New indicator (IOC_NEW)
                event_type: IntelligenceEventTypeLiteral = "IOC_NEW"
                severity: AlertSeverityLiteral = "HIGH" if obs.classification == "MALICIOUS" else "INFORMATIONAL"
                changes.append(
                    IntelligenceChangeEventDTO(
                        event_id=f"ev_new_{uuid.uuid4().hex[:12]}",
                        event_type=event_type,
                        entity_id=obs.indicator_value_hash,
                        previous_state="DISCOVERED",
                        new_state=obs.classification,
                        source=obs.feed_id,
                        confidence=obs.confidence,
                        feed_version=obs.feed_version,
                        provenance=f"Newly discovered {obs.indicator_type} indicator in feed {obs.feed_id}",
                        severity=severity,
                        status="ACTIVE",
                    )
                )
            else:
                # Check for classification change (e.g. BENIGN -> MALICIOUS or MALICIOUS -> BENIGN)
                if historical.classification != obs.classification:
                    event_type = "IOC_RECLASSIFIED"
                    severity = "CRITICAL" if obs.classification == "MALICIOUS" else "LOW"
                    changes.append(
                        IntelligenceChangeEventDTO(
                            event_id=f"ev_reclass_{uuid.uuid4().hex[:12]}",
                            event_type=event_type,
                            entity_id=obs.indicator_value_hash,
                            previous_state=historical.classification,
                            new_state=obs.classification,
                            source=obs.feed_id,
                            confidence=obs.confidence,
                            feed_version=obs.feed_version,
                            provenance=f"Indicator reclassified from {historical.classification} to {obs.classification} by {obs.feed_id}",
                            severity=severity,
                            status="ACTIVE",
                        )
                    )
                elif historical.status != obs.status:
                    # Status change (e.g. ACTIVE -> REVOKED)
                    event_type = "IOC_REVOKED" if obs.status == "REVOKED" else "IOC_UPDATED"
                    changes.append(
                        IntelligenceChangeEventDTO(
                            event_id=f"ev_status_{uuid.uuid4().hex[:12]}",
                            event_type=event_type,
                            entity_id=obs.indicator_value_hash,
                            previous_state=historical.status,
                            new_state=obs.status,
                            source=obs.feed_id,
                            confidence=obs.confidence,
                            feed_version=obs.feed_version,
                            provenance=f"Indicator status changed from {historical.status} to {obs.status}",
                            severity="MEDIUM",
                            status="ACTIVE",
                        )
                    )

        return changes
