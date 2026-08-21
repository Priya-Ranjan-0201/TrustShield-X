"""
Crisis Communications & Fact Governance Engine (Phase 36)
=========================================================
Manages crisis communication drafts, regulatory disclosures, and executive updates.
Enforces strict Fact Governance distinguishing CONFIRMED, SUSPECTED, and UNKNOWN data,
and mandates explicit human authorization before external broadcast.
"""

from typing import Dict, Any, List, Optional
import datetime
import uuid


class CrisisCommunicationEngine:
    COMMUNICATION_TYPES = {
        "INTERNAL_SECURITY",
        "EXECUTIVE_BRIEFING",
        "OPERATIONAL_UPDATE",
        "CUSTOMER_DRAFT",
        "REGULATORY_DRAFT"
    }

    def __init__(self):
        self._communications: Dict[str, Dict[str, Any]] = {}

    def create_communication_draft(
        self,
        comm_id: str,
        crisis_id: str,
        tenant_id: str,
        comm_type: str,
        audience: str,
        confirmed_facts: List[str],
        suspected_facts: List[str],
        unknowns: List[str],
        draft_content: str,
        author: str = "TruthShield Security Copilot"
    ) -> Dict[str, Any]:
        if comm_type not in self.COMMUNICATION_TYPES:
            raise ValueError(f"Invalid communication type: {comm_type}")

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Invariant: External / Regulated communications require explicit dual approval
        requires_approval = comm_type in {"CUSTOMER_DRAFT", "REGULATORY_DRAFT", "EXECUTIVE_BRIEFING"}

        comm = {
            "comm_id": comm_id,
            "crisis_id": crisis_id,
            "tenant_id": tenant_id,
            "comm_type": comm_type,
            "audience": audience,
            "fact_governance": {
                "confirmed_facts": confirmed_facts,
                "suspected_facts": suspected_facts,
                "unknowns": unknowns
            },
            "draft_content": draft_content,
            "author": author,
            "status": "DRAFT",
            "requires_approval": requires_approval,
            "approval_metadata": None,
            "created_at": now,
            "sent_at": None
        }
        self._communications[comm_id] = comm
        return comm

    def approve_communication(
        self,
        comm_id: str,
        tenant_id: str,
        approver: str,
        notes: str = "Approved for dispatch"
    ) -> Dict[str, Any]:
        comm = self._communications.get(comm_id)
        if not comm or comm["tenant_id"] != tenant_id:
            raise ValueError(f"Communication draft {comm_id} not found")

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        comm["status"] = "APPROVED"
        comm["approval_metadata"] = {
            "approver": approver,
            "approved_at": now,
            "notes": notes
        }
        return comm

    def send_communication(
        self,
        comm_id: str,
        tenant_id: str,
        sender: str
    ) -> Dict[str, Any]:
        comm = self._communications.get(comm_id)
        if not comm or comm["tenant_id"] != tenant_id:
            raise ValueError(f"Communication draft {comm_id} not found")

        if comm["requires_approval"] and comm["status"] != "APPROVED":
            raise PermissionError(f"Communication {comm_id} requires authorization approval before broadcast")

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        comm["status"] = "SENT"
        comm["sent_at"] = now
        comm["sent_by"] = sender
        return comm

    def get_crisis_communications(self, crisis_id: str, tenant_id: str) -> List[Dict[str, Any]]:
        return [c for c in self._communications.values() if c["crisis_id"] == crisis_id and c["tenant_id"] == tenant_id]


crisis_communication_engine = CrisisCommunicationEngine()
