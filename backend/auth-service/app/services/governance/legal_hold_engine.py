"""Legal Hold & Evidence Preservation Engine (Phase 4.0 Part 8 — Sections 34-35, 96).

Manages active legal holds that unconditionally shield resources from automated retention deletion.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.governance_models import LegalHoldDTO


class LegalHoldEngine:
    """Manages legal holds on forensic evidence, cases, incidents, and reports."""

    def __init__(self):
        self._holds: Dict[str, LegalHoldDTO] = {}
        self._resource_to_hold: Dict[str, str] = {}

    def apply_legal_hold(
        self,
        organization_id: str,
        resource_type: str,
        resource_id: str,
        reason: str,
        created_by: str,
        approved_by: Optional[str] = None,
    ) -> LegalHoldDTO:
        hold = LegalHoldDTO(
            hold_id=f"hold_{uuid.uuid4().hex[:12]}",
            organization_id=organization_id,
            resource_type=resource_type,
            resource_id=resource_id,
            reason=reason,
            created_by=created_by,
            approved_by=approved_by,
            status="ACTIVE",
        )
        self._holds[hold.hold_id] = hold
        self._resource_to_hold[resource_id] = hold.hold_id
        return hold

    def release_legal_hold(self, hold_id: str, released_by: str) -> Optional[LegalHoldDTO]:
        hold = self._holds.get(hold_id)
        if hold:
            hold.status = "RELEASED"
            hold.released_at = datetime.now(timezone.utc).isoformat()
            self._resource_to_hold.pop(hold.resource_id, None)
        return hold

    def is_under_legal_hold(self, resource_id: str) -> bool:
        """Section 35, Mandatory Test 8, 15: Returns True if resource has an ACTIVE legal hold."""
        hold_id = self._resource_to_hold.get(resource_id)
        if not hold_id:
            return False
        hold = self._holds.get(hold_id)
        return hold is not None and hold.status == "ACTIVE"

    def get_hold(self, hold_id: str) -> Optional[LegalHoldDTO]:
        return self._holds.get(hold_id)

    def list_holds(self, organization_id: Optional[str] = None) -> List[LegalHoldDTO]:
        if organization_id:
            return [h for h in self._holds.values() if h.organization_id == organization_id]
        return list(self._holds.values())
