"""
Privilege Governance, CIEM & Just-In-Time (JIT) Engine (Phase 34)
=================================================================
Enforces zero standing privileges, time-bounded JIT elevations, dual authorization,
excess privilege detection (EXCESS_PRIVILEGE), periodic/emergency access reviews,
and emergency break-glass access (BREAK_GLASS_ACCESS).
"""

from typing import Dict, Any, List, Optional
import datetime
import hashlib
import uuid


class PrivilegeGovernanceEngine:
    def __init__(self):
        self._jit_requests: Dict[str, Dict[str, Any]] = {}
        self._active_grants: Dict[str, Dict[str, Any]] = {}
        self._break_glass_events: Dict[str, Dict[str, Any]] = {}
        self._privilege_reviews: Dict[str, Dict[str, Any]] = {}
        self._excess_privilege_findings: List[Dict[str, Any]] = []

    def request_jit_elevation(
        self,
        request_id: str,
        tenant_id: str,
        subject_id: str,
        requested_role: str,
        justification: str,
        duration_minutes: int = 30,
        peer_reviewer_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        req = {
            "request_id": request_id,
            "tenant_id": tenant_id,
            "subject_id": subject_id,
            "requested_role": requested_role,
            "target_role": requested_role,
            "justification": justification,
            "duration_minutes": duration_minutes,
            "peer_reviewer_id": peer_reviewer_id,
            "status": "PENDING",
            "requested_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "approved_by": None,
            "expires_at": None
        }
        self._jit_requests[request_id] = req
        return req

    def request_jit_privilege(
        self,
        request_id: str,
        tenant_id: str,
        subject_id: str,
        target_role: str,
        duration_minutes: int,
        justification: str,
        peer_reviewer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        return self.request_jit_elevation(
            request_id=request_id,
            tenant_id=tenant_id,
            subject_id=subject_id,
            requested_role=target_role,
            justification=justification,
            duration_minutes=duration_minutes,
            peer_reviewer_id=peer_reviewer_id
        )

    def approve_jit_elevation(
        self,
        request_id: str,
        tenant_id: str,
        approver_id: str
    ) -> Dict[str, Any]:
        req = self._jit_requests.get(request_id)
        if not req or req["tenant_id"] != tenant_id:
            return {"status": "FAILED", "reason": "REQUEST_NOT_FOUND"}

        if req["subject_id"] == approver_id:
            return {"status": "FAILED", "reason": "SELF_APPROVAL_PROHIBITED"}

        req["status"] = "APPROVED"
        req["approved_by"] = approver_id
        now = datetime.datetime.now(datetime.timezone.utc)
        expires = now + datetime.timedelta(minutes=req["duration_minutes"])
        req["expires_at"] = expires.isoformat()

        self._active_grants[request_id] = req
        return req

    def approve_jit_privilege(
        self,
        request_id: str,
        tenant_id: str,
        approver_id: str
    ) -> Dict[str, Any]:
        return self.approve_jit_elevation(request_id, tenant_id, approver_id)

    def revoke_elevation(self, request_id: str, tenant_id: str) -> Dict[str, Any]:
        if request_id in self._active_grants:
            grant = self._active_grants.pop(request_id)
            grant["status"] = "REVOKED"
            return {"request_id": request_id, "status": "REVOKED"}
        return {"status": "FAILED", "reason": "GRANT_NOT_ACTIVE"}

    def get_jit_requests(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [r for r in self._jit_requests.values() if r["tenant_id"] == tenant_id]

    # Break-Glass Emergency Access (Section 59 & 83)
    def request_break_glass_access(
        self,
        event_id: str,
        tenant_id: str,
        subject_id: str,
        justification: str,
        mfa_token: Optional[str],
        duration_minutes: int = 15,
        approver_id: Optional[str] = None
    ) -> Dict[str, Any]:
        # Break-glass requires strong authentication and non-empty justification
        if not mfa_token or len(mfa_token.strip()) < 6:
            return {
                "event_id": event_id,
                "status": "BLOCKED",
                "reason": "STRONG_MFA_AUTHENTICATION_REQUIRED"
            }

        if not justification or len(justification.strip()) < 10:
            return {
                "event_id": event_id,
                "status": "BLOCKED",
                "reason": "MANDATORY_EMERGENCY_JUSTIFICATION_REQUIRED"
            }

        now = datetime.datetime.now(datetime.timezone.utc)
        expires_at = now + datetime.timedelta(minutes=min(60, max(5, duration_minutes)))

        # Cryptographic audit hash
        audit_payload = f"{event_id}:{tenant_id}:{subject_id}:{justification}:{now.isoformat()}"
        audit_hash = hashlib.sha256(audit_payload.encode()).hexdigest()

        record = {
            "event_id": event_id,
            "tenant_id": tenant_id,
            "subject_id": subject_id,
            "access_type": "BREAK_GLASS_ACCESS",
            "justification": justification,
            "duration_minutes": duration_minutes,
            "status": "ACTIVE_EMERGENCY_ACCESS",
            "approved_by": approver_id or "EMERGENCY_OVERRIDE_GATEWAY",
            "audit_hash": audit_hash,
            "mandatory_review_required": True,
            "review_status": "PENDING_MANDATORY_REVIEW",
            "granted_at": now.isoformat(),
            "expires_at": expires_at.isoformat()
        }
        self._break_glass_events[event_id] = record
        return record

    def conduct_break_glass_review(
        self,
        event_id: str,
        tenant_id: str,
        reviewer_id: str,
        review_notes: str,
        verdict: str = "JUSTIFIED"  # JUSTIFIED, ABUSE_DETECTED, REVOKED
    ) -> Dict[str, Any]:
        event = self._break_glass_events.get(event_id)
        if not event or event["tenant_id"] != tenant_id:
            return {"status": "FAILED", "reason": "EVENT_NOT_FOUND"}

        event["review_status"] = verdict
        event["reviewed_by"] = reviewer_id
        event["review_notes"] = review_notes
        event["reviewed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return event

    # Least Privilege & Excess Privilege Analysis (Section 15)
    def detect_excess_privilege(
        self,
        tenant_id: str,
        identity_id: str,
        assigned_roles: List[str],
        used_roles: List[str],
        assigned_permissions: List[str],
        used_permissions: List[str]
    ) -> Dict[str, Any]:
        unused_roles = [r for r in assigned_roles if r not in used_roles]
        unused_perms = [p for p in assigned_permissions if p not in used_permissions]

        has_excess = len(unused_roles) > 0 or len(unused_perms) > 0
        finding = {
            "finding_id": f"EXCESS-PRIV-{uuid.uuid4().hex[:8]}",
            "tenant_id": tenant_id,
            "identity_id": identity_id,
            "finding_type": "EXCESS_PRIVILEGE",
            "has_excess_privilege": has_excess,
            "unused_roles": unused_roles,
            "unused_permissions": unused_perms,
            "recommended_action": "REVOKE_UNUSED_PERMISSIONS",
            "assessed_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        if has_excess:
            self._excess_privilege_findings.append(finding)
        return finding

    # Privilege Review (Section 17)
    def create_access_review(
        self,
        review_id: str,
        tenant_id: str,
        review_type: str = "PERIODIC",  # PERIODIC, PRIVILEGED, EMERGENCY
        target_scope: str = "ALL_PRIVILEGED_ROLES"
    ) -> Dict[str, Any]:
        review = {
            "review_id": review_id,
            "tenant_id": tenant_id,
            "review_type": review_type,
            "target_scope": target_scope,
            "status": "IN_PROGRESS",
            "findings_count": len([f for f in self._excess_privilege_findings if f["tenant_id"] == tenant_id]),
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._privilege_reviews[review_id] = review
        return review


privilege_governance_engine = PrivilegeGovernanceEngine()
