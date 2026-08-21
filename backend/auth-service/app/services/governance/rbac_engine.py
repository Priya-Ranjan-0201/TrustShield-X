"""Enterprise RBAC Engine & Least Privilege Governance (Phase 4.0 Part 8 — Sections 8-13, 92).

Enforces role-based permissions ('resource:action'), permission scopes, and least-privilege defaults.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
import hashlib
import json
import uuid
from datetime import datetime, timezone
from app.schemas.governance_models import (
    RoleDTO,
    RoleVersionDTO,
    PermissionDTO,
    PermissionScopeLiteral,
    SystemRoleLiteral,
    AuthorizationDecisionDTO,
)

DEFAULT_SYSTEM_ROLES: Dict[str, List[str]] = {
    "SUPER_ADMIN": ["*:*"],
    "ORG_ADMIN": [
        "user:*", "role:*", "policy:*", "incident:*", "alert:*", "report:*",
        "evidence:*", "compliance:*", "audit:read", "export:*", "retention:*", "session:*", "api_key:*"
    ],
    "SECURITY_ADMIN": [
        "policy:*", "incident:*", "alert:*", "response:approve", "response:simulate",
        "evidence:read", "audit:read", "compliance:read", "session:revoke", "api_key:revoke"
    ],
    "SOC_ANALYST": [
        "incident:read", "incident:update", "incident:assign", "alert:read", "alert:acknowledge",
        "response:simulate", "evidence:read", "evidence:collect", "report:read"
    ],
    "SENIOR_ANALYST": [
        "incident:read", "incident:update", "incident:assign", "incident:merge", "incident:split",
        "alert:read", "alert:acknowledge", "alert:escalate", "response:simulate", "response:execute",
        "evidence:read", "evidence:collect", "report:read", "report:export"
    ],
    "INVESTIGATOR": [
        "case:*", "incident:read", "evidence:read", "evidence:collect", "report:read", "report:create"
    ],
    "THREAT_INTELLIGENCE_ANALYST": [
        "intelligence:*", "feed:*", "campaign:*", "indicator:*", "incident:read", "alert:read"
    ],
    "INCIDENT_RESPONDER": [
        "incident:read", "incident:update", "response:simulate", "response:execute", "response:rollback",
        "evidence:read", "evidence:collect"
    ],
    "AUDITOR": [
        "audit:read", "compliance:read", "policy:read", "report:read", "evidence:read"
    ],
    "COMPLIANCE_OFFICER": [
        "compliance:*", "audit:read", "policy:read", "retention:*", "legal_hold:*", "privacy:*", "report:read"
    ],
    "REPORT_VIEWER": [
        "report:read"
    ],
    "READ_ONLY_USER": [
        "incident:read", "alert:read", "report:read"
    ],
}

# Explicitly prohibited actions for non-privileged roles (Section 10, Mandatory Tests 3, 4)
NON_EXECUTOR_ROLES = {"REPORT_VIEWER", "READ_ONLY_USER", "AUDITOR", "COMPLIANCE_OFFICER"}


class RBACEngine:
    """Manages role definitions, immutable versioning, permission resolution, and least privilege checks."""

    def __init__(self):
        self._roles: Dict[str, RoleDTO] = {}
        self._role_versions: Dict[str, RoleVersionDTO] = {}
        self._initialize_default_roles()

    def _initialize_default_roles(self):
        for role_name, perms in DEFAULT_SYSTEM_ROLES.items():
            role = RoleDTO(
                role_id=f"role_{role_name.lower()}",
                name=role_name,
                description=f"Standard system role for {role_name}",
                system_role=True,
                permissions=perms,
                scope="ORGANIZATION",
                version=1,
            )
            self._roles[role.role_id] = role
            self._roles[role_name] = role  # Alias by name

    def create_or_update_role(
        self,
        name: str,
        permissions: List[str],
        organization_id: Optional[str] = None,
        description: str = "",
        scope: PermissionScopeLiteral = "ORGANIZATION",
        created_by: str = "ADMIN",
    ) -> Tuple[RoleDTO, RoleVersionDTO]:
        """Creates or publishes a new immutable version of an RBAC role (Section 8, 21)."""
        # Calculate SHA-256 content hash
        perms_sorted = sorted(set(permissions))
        content_hash = hashlib.sha256(json.dumps(perms_sorted).encode()).hexdigest()

        role_id = f"role_{name.lower().replace(' ', '_')}"
        existing = self._roles.get(role_id)
        ver_num = (existing.version + 1) if existing else 1

        role = RoleDTO(
            role_id=role_id,
            organization_id=organization_id,
            name=name,
            description=description,
            system_role=False,
            permissions=perms_sorted,
            scope=scope,
            version=ver_num,
            created_by=created_by,
        )
        self._roles[role_id] = role
        self._roles[name] = role

        ver_dto = RoleVersionDTO(
            version_id=f"rlv_{role_id}_v{ver_num}",
            role_id=role_id,
            version_number=ver_num,
            content_hash=content_hash,
            permissions=perms_sorted,
            created_by=created_by,
        )
        self._role_versions[ver_dto.version_id] = ver_dto
        return role, ver_dto

    def get_effective_permissions(self, role_names: List[str]) -> Set[str]:
        perms = set()
        for r_name in role_names:
            role = self._roles.get(r_name) or self._roles.get(f"role_{r_name.lower()}")
            if role:
                perms.update(role.permissions)
        return perms

    def has_permission(
        self,
        user_roles: List[str],
        required_resource: str,
        required_action: str,
    ) -> bool:
        """Check if user roles grant requested resource:action with wildcard support."""
        # 1. Least Privilege Check for Non-Executors (Section 10, Mandatory Tests 3, 4)
        if required_action in ("execute", "delete", "rollback", "destroy"):
            # If user ONLY has read-only or auditor roles, deny execution
            if user_roles and all(r in NON_EXECUTOR_ROLES for r in user_roles):
                return False

        effective_perms = self.get_effective_permissions(user_roles)

        req_str = f"{required_resource}:{required_action}"
        if "*:*" in effective_perms:
            return True
        if req_str in effective_perms:
            return True
        if f"{required_resource}:*" in effective_perms:
            return True
        if f"*:{required_action}" in effective_perms:
            return True
        return False

    def evaluate_rbac_access(
        self,
        user_id: str,
        user_roles: List[str],
        resource: str,
        action: str,
        resource_org_id: Optional[str] = None,
        user_org_id: Optional[str] = None,
    ) -> AuthorizationDecisionDTO:
        """Evaluates RBAC access and provides an explainable decision without leaking internals."""
        # 1. Multi-Tenant Check (Section 4, Mandatory Tests 1, 2)
        if resource_org_id and user_org_id and resource_org_id != user_org_id:
            # Super admins with GLOBAL scope can be allowed, but by default cross-tenant is DENIED
            if "SUPER_ADMIN" not in user_roles:
                return AuthorizationDecisionDTO(
                    allowed=False,
                    decision="DENY",
                    reason="Access denied: Cross-tenant resource access is prohibited.",
                    required_permissions=[f"{resource}:{action}"],
                )

        # 2. Permission Check
        allowed = self.has_permission(user_roles, resource, action)
        if not allowed:
            return AuthorizationDecisionDTO(
                allowed=False,
                decision="DENY",
                reason=f"User lacks required permission: '{resource}:{action}'.",
                required_permissions=[f"{resource}:{action}"],
            )

        return AuthorizationDecisionDTO(
            allowed=True,
            decision="ALLOW",
            reason=f"Authorized by role assignment for '{resource}:{action}'.",
            matched_rules=list(self.get_effective_permissions(user_roles)),
        )

    def get_role(self, role_id_or_name: str) -> Optional[RoleDTO]:
        return self._roles.get(role_id_or_name) or self._roles.get(f"role_{role_id_or_name.lower()}")

    def list_roles(self) -> List[RoleDTO]:
        # Return unique roles
        seen = set()
        out = []
        for r in self._roles.values():
            if r.role_id not in seen:
                seen.add(r.role_id)
                out.append(r)
        return out
