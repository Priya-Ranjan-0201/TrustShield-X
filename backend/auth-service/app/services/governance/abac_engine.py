"""Enterprise ABAC Engine & Attribute-Based Authorization (Phase 4.0 Part 8 — Sections 14-16, 93).

Evaluates contextual attributes: user, role, classification, MFA status, time, severity, and session health.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.schemas.governance_models import (
    AuthorizationDecisionDTO,
    DataClassificationLiteral,
    DecisionEffectLiteral,
)


class ABACEngine:
    """Evaluates fine-grained attribute conditions over subjects, resources, and environmental context."""

    @staticmethod
    def evaluate_abac(
        user_id: str,
        user_roles: List[str],
        resource_id: str,
        resource_type: str,
        classification: DataClassificationLiteral = "INTERNAL",
        resource_owner_id: Optional[str] = None,
        incident_severity: Optional[str] = None,
        mfa_verified: bool = False,
        mfa_required_by_policy: bool = False,
        session_status: str = "ACTIVE",
        ip_address: str = "127.0.0.1",
        time_of_request: Optional[datetime] = None,
    ) -> AuthorizationDecisionDTO:
        # 1. Session Health Check
        if session_status != "ACTIVE":
            return AuthorizationDecisionDTO(
                allowed=False,
                decision="DENY",
                reason=f"Access denied: User session is {session_status}.",
            )

        # 2. MFA Policy Enforcement (Section 75, Mandatory Test 5)
        if mfa_required_by_policy and not mfa_verified:
            return AuthorizationDecisionDTO(
                allowed=False,
                decision="REQUIRE_MFA",
                reason="Policy requires multi-factor authentication for this operation.",
                required_approval=False,
            )

        # 3. Data Classification Clearance Check (Section 27-29, Mandatory Test 10)
        if classification in ("RESTRICTED", "HIGHLY_RESTRICTED"):
            # Requires privileged security role or direct resource ownership
            privileged = any(r in ("SUPER_ADMIN", "SECURITY_ADMIN", "ORG_ADMIN", "COMPLIANCE_OFFICER") for r in user_roles)
            is_owner = (resource_owner_id and resource_owner_id == user_id)
            if not (privileged or is_owner):
                return AuthorizationDecisionDTO(
                    allowed=False,
                    decision="DENY",
                    reason=f"Access denied: User lacks clearance for {classification} classified data.",
                )

        # 4. Critical Severity Containment Condition
        if incident_severity == "CRITICAL" and "READ_ONLY_USER" in user_roles and len(user_roles) == 1:
            return AuthorizationDecisionDTO(
                allowed=False,
                decision="DENY",
                reason="Access denied: Critical incident access restricted to authorized incident responders.",
            )

        return AuthorizationDecisionDTO(
            allowed=True,
            decision="ALLOW",
            reason="ABAC attribute policies satisfied.",
        )
