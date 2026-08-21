"""
TruthShield X — Intelligence Conflict Detection & Resolution Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.federation_models import IntelligenceConflictDTO, ConflictStateLiteral


class IntelligenceConflictEngine:
    """Detects contradictions between disparate intelligence sources and manages forensic resolution workflows."""

    def __init__(self):
        # conflict_id -> IntelligenceConflictDTO
        self._conflicts: Dict[str, IntelligenceConflictDTO] = {}

    def detect_and_register_conflict(
        self,
        canonical_identifier: str,
        claims: List[Dict[str, Any]],
    ) -> Optional[IntelligenceConflictDTO]:
        """Detects whether contradictory claims exist for a single indicator."""
        has_malicious = any(c.get("classification") in ("MALICIOUS", "PHISHING", "SUSPICIOUS") for c in claims)
        has_benign = any(c.get("classification") in ("BENIGN", "SAFE", "TRUSTED") for c in claims)

        if not (has_malicious and has_benign):
            return None  # No contradiction detected

        conflict_id = f"cnf_{uuid.uuid4().hex[:10]}"
        conflict = IntelligenceConflictDTO(
            conflict_id=conflict_id,
            canonical_identifier=canonical_identifier,
            conflicting_claims=claims,
            resolution_state="UNRESOLVED",
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        self._conflicts[conflict_id] = conflict
        return conflict

    def resolve_conflict(
        self,
        conflict_id: str,
        resolution_state: ConflictStateLiteral,
        resolution_notes: str,
        resolved_by: str,
    ) -> IntelligenceConflictDTO:
        """Resolves an intelligence conflict with immutable analyst notes."""
        conflict = self._conflicts.get(conflict_id)
        if not conflict:
            raise KeyError(f"Conflict '{conflict_id}' not found.")

        conflict.resolution_state = resolution_state
        conflict.resolution_notes = resolution_notes
        conflict.resolved_by = resolved_by
        conflict.resolved_at = datetime.now(timezone.utc).isoformat()
        return conflict

    def list_conflicts(self, unresolved_only: bool = False) -> List[IntelligenceConflictDTO]:
        """Lists registered intelligence conflicts."""
        if unresolved_only:
            return [c for c in self._conflicts.values() if c.resolution_state == "UNRESOLVED"]
        return list(self._conflicts.values())
