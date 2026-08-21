"""
TruthShield X — Defense Playbook Registry (Phase 28).

Maintains version-controlled, validated, and sanitized collective defensive playbooks.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


class DefensePlaybookRegistry:
    """Manages versioned and peer-validated coordination playbooks."""

    def __init__(self):
        self._playbooks: Dict[str, Dict[str, Any]] = {}
        self._seed_default_playbook()

    def _seed_default_playbook(self):
        pb1 = {
            "playbook_id": "pbk_darkstorm_credential_mitigation",
            "version": "1.2.0",
            "title": "DarkStorm Credential Stuffing Joint Mitigation Playbook",
            "description": "Multi-tenant synchronized rate-limiting, step-up MFA enforcement, and ASN blocking.",
            "target_techniques": ["T1078", "T1055"],
            "steps": [
                {"step_num": 1, "description": "Verify C2 hash indicators across edge proxies"},
                {"step_num": 2, "description": "Trigger Phase 26 Digital Twin sandbox containment test"},
                {"step_num": 3, "description": "Apply edge WAF rate-limiting rule upon Four-Eyes approval"},
            ],
            "rollback_procedure": "Automated route restoration script",
            "validated_by": "TruthShield X Core Engineering",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._playbooks[pb1["playbook_id"]] = pb1

    def get_playbook(self, playbook_id: str) -> Optional[Dict[str, Any]]:
        return self._playbooks.get(playbook_id)

    def list_playbooks(self) -> List[Dict[str, Any]]:
        return list(self._playbooks.values())
