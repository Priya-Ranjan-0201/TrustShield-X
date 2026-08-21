"""
TruthShield X — Secure Playbook Engine (Phase 21).

Manages versioned, test-validated SOAR defensive playbooks.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.autonomous_soc_models import SecurePlaybookDTO, PlaybookNodeDTO


class SecurePlaybookEngine:
    """Manages secure versioned SOAR playbooks and dry-run execution."""

    def __init__(self):
        self._playbooks: Dict[str, SecurePlaybookDTO] = {}
        self._initialize_default_playbooks()

    def _initialize_default_playbooks(self):
        nodes = [
            PlaybookNodeDTO(node_id="n1", node_type="TRIGGER", name="Alert Ingested", next_node_ids=["n2"]),
            PlaybookNodeDTO(node_id="n2", node_type="SIMULATE", name="Dry-Run Twin Simulation", next_node_ids=["n3"]),
            PlaybookNodeDTO(node_id="n3", node_type="APPROVAL", name="Four-Eyes Approval", requires_approval=True, next_node_ids=["n4"]),
            PlaybookNodeDTO(node_id="n4", node_type="ACTION", name="Isolate Host", next_node_ids=["n5"]),
            PlaybookNodeDTO(node_id="n5", node_type="VERIFY", name="Verify State", next_node_ids=["n6"]),
            PlaybookNodeDTO(node_id="n6", node_type="END", name="Complete Playbook"),
        ]
        pb = SecurePlaybookDTO(
            playbook_id="pb_phishing_containment",
            tenant_id="default_tenant",
            version=1,
            name="Automated Phishing Containment Playbook",
            owner="usr_soc_lead",
            approval_status="APPROVED",
            test_status="VERIFIED",
            nodes=nodes,
            rollback_strategy=["Unblock domain in DNS sinkhole", "Notify analyst"],
            last_reviewed=datetime.now(timezone.utc).isoformat(),
        )
        self._playbooks[pb.playbook_id] = pb

    def get_playbook(self, playbook_id: str) -> Optional[SecurePlaybookDTO]:
        return self._playbooks.get(playbook_id)

    def list_playbooks(self, tenant_id: str = "default_tenant") -> List[SecurePlaybookDTO]:
        return [p for p in self._playbooks.values() if p.tenant_id == tenant_id]

    def register_playbook(self, playbook: SecurePlaybookDTO) -> SecurePlaybookDTO:
        self._playbooks[playbook.playbook_id] = playbook
        return playbook
