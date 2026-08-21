"""
TruthShield X — Digital Twin Governance Engine (Phase 26).

Enforces RBAC/ABAC permissions and maintains immutable SHA-256 audit logs for simulation activities.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone
import hashlib
import json


class TwinGovernanceEngine:
    """Manages access control and cryptographic audit chaining for the digital twin simulation lab."""

    def __init__(self):
        self._audit_log: List[Dict[str, Any]] = []

    def check_permission(self, user_role: str, action: str) -> bool:
        role_permissions = {
            "ADMIN": ["twin.read", "twin.create", "twin.simulate", "twin.compare", "twin.export", "twin.admin"],
            "CISO": ["twin.read", "twin.create", "twin.simulate", "twin.compare", "twin.export", "twin.admin"],
            "SOC_ANALYST": ["twin.read", "twin.simulate", "twin.compare"],
            "AUDITOR": ["twin.read", "twin.export"],
        }
        allowed = role_permissions.get(user_role, [])
        return action in allowed

    def log_simulation_audit(self, action: str, details: Dict[str, Any], tenant_id: str = "default_tenant") -> str:
        prev_hash = self._audit_log[-1]["entry_hash"] if self._audit_log else "GENESIS_HASH_TWIN"
        payload = {
            "action": action,
            "details": details,
            "tenant_id": tenant_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prev_hash": prev_hash,
        }
        entry_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        entry = {**payload, "entry_hash": entry_hash}
        self._audit_log.append(entry)
        return entry_hash
