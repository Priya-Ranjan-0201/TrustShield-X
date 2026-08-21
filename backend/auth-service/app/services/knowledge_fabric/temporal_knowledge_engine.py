"""
TruthShield X — Temporal Knowledge Engine (Phase 19).

Tracks knowledge temporal intervals: CURRENT, HISTORICAL, FUTURE_PREDICTED, SIMULATED.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.cyber_knowledge_fabric_models import (
    TemporalKnowledgeDTO,
    TemporalStateLiteral,
)


class TemporalKnowledgeEngine:
    """Manages multi-temporal states, time windows, and prevents silent historical overwrites."""

    def __init__(self):
        self._temporal_records: Dict[str, List[TemporalKnowledgeDTO]] = {}

    def record_temporal_state(
        self,
        object_id: str,
        temporal_state: TemporalStateLiteral = "CURRENT",
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None,
        observed_at: Optional[str] = None,
    ) -> TemporalKnowledgeDTO:
        """Records a temporal observation interval."""
        now_iso = datetime.now(timezone.utc).isoformat()
        rec = TemporalKnowledgeDTO(
            object_id=object_id,
            temporal_state=temporal_state,
            valid_from=valid_from or now_iso,
            valid_until=valid_until,
            observed_at=observed_at or now_iso,
            recorded_at=now_iso,
        )
        if object_id not in self._temporal_records:
            self._temporal_records[object_id] = []
        self._temporal_records[object_id].append(rec)
        return rec

    def get_temporal_history(self, object_id: str) -> List[TemporalKnowledgeDTO]:
        """Returns all recorded temporal states for an object."""
        return self._temporal_records.get(object_id, [])

    def get_current_state(self, object_id: str) -> Optional[TemporalKnowledgeDTO]:
        """Returns latest CURRENT temporal record."""
        history = self._temporal_records.get(object_id, [])
        currents = [r for r in history if r.temporal_state == "CURRENT"]
        return currents[-1] if currents else None
