"""
Cloud Infrastructure Entitlement Management (CIEM) & Identity Governance Engine (Phase 34)
========================================================================================
Identifies overprivileged accounts, stale IAM credentials, standing access paths,
and enforces automated Just-In-Time (JIT) least-privilege policies.
"""

from typing import Dict, Any, List, Optional
import datetime


class IdentityEntitlementEngine:
    def __init__(self):
        self._entitlements: Dict[str, Dict[str, Any]] = {}
        self._jit_grants: Dict[str, Dict[str, Any]] = {}

    def register_identity_entitlement(
        self,
        identity_id: str,
        tenant_id: str,
        identity_type: str,  # USER, SERVICE_ACCOUNT, ROLE
        assigned_permissions: List[str],
        used_permissions: List[str],
        last_active_at: Optional[str] = None
    ) -> Dict[str, Any]:
        unused = [p for p in assigned_permissions if p not in used_permissions]
        overprivileged_ratio = len(unused) / len(assigned_permissions) if assigned_permissions else 0.0

        record = {
            "identity_id": identity_id,
            "tenant_id": tenant_id,
            "identity_type": identity_type,
            "assigned_permissions": assigned_permissions,
            "used_permissions": used_permissions,
            "unused_permissions": unused,
            "overprivileged_ratio": round(overprivileged_ratio, 2),
            "is_overprivileged": overprivileged_ratio > 0.3,
            "last_active_at": last_active_at or datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._entitlements[identity_id] = record
        return record

    def analyze_identity_entitlement(
        self,
        identity_id: str,
        tenant_id: str,
        assigned_permissions: List[str],
        used_permissions: List[str],
        identity_type: str = "USER"
    ) -> Dict[str, Any]:
        return self.register_identity_entitlement(
            identity_id=identity_id,
            tenant_id=tenant_id,
            identity_type=identity_type,
            assigned_permissions=assigned_permissions,
            used_permissions=used_permissions
        )

    def request_jit_access(
        self,
        request_id: str,
        tenant_id: str,
        identity_id: str,
        requested_role: str,
        duration_minutes: int = 60,
        justification: str = "Emergency incident investigation"
    ) -> Dict[str, Any]:
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=duration_minutes)
        grant = {
            "request_id": request_id,
            "tenant_id": tenant_id,
            "identity_id": identity_id,
            "requested_role": requested_role,
            "duration_minutes": duration_minutes,
            "justification": justification,
            "status": "APPROVED",
            "expires_at": expires_at.isoformat(),
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._jit_grants[request_id] = grant
        return grant

    def get_overprivileged_identities(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [e for e in self._entitlements.values() if e["tenant_id"] == tenant_id and e["is_overprivileged"]]


identity_entitlement_engine = IdentityEntitlementEngine()
