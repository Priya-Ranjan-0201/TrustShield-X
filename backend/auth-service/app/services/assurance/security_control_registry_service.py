"""
TruthShield X — Security Control Registry Service
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.assurance_models import (
    SecurityControlRegistryDTO,
    ControlCategoryLiteral,
    ControlLifecycleLiteral,
    VerificationStateLiteral,
)


class SecurityControlRegistryService:
    """Manages the lifecycle, metadata, and empirical verification state of all platform security controls."""

    def __init__(self):
        # control_id -> SecurityControlRegistryDTO
        self._controls: Dict[str, SecurityControlRegistryDTO] = {}
        self._initialize_core_controls()

    def _initialize_core_controls(self) -> None:
        """Seeds initial flagship platform security controls."""
        core_controls = [
            ("ctrl_iso_01", "Tenant Data Isolation Boundary", "TENANT_ISOLATION", "Enforces cryptographic and partition-level isolation across all multi-tenant queries."),
            ("ctrl_rbac_01", "ABAC / RBAC Explicit Deny Precedence", "ACCESS_CONTROL", "Guarantees explicit DENY overrides any permission grant."),
            ("ctrl_audit_01", "SHA-256 Immutability Audit Chain", "AUDIT", "Maintains tamper-evident append-only cryptographic log continuity."),
            ("ctrl_waf_01", "Edge Threat WAF & Rate Limiting", "PREVENTIVE", "Blocks known malicious indicators and throttles anomalous request bursts."),
            ("ctrl_dr_01", "Database Replication & Standby Failover", "DISASTER_RECOVERY", "Ensures standby database promotion within recovery objectives."),
            ("ctrl_ai_01", "AI Copilot Safety & Grounding Boundary", "AI_SECURITY", "Prevents prompt injection, hallucinated evidence, and unauthorized actions."),
            ("ctrl_sim_01", "Digital Twin Zero-Mutation Guard", "GOVERNANCE", "Blocks simulation environments from mutating production databases or graphs."),
        ]

        for cid, name, cat, desc in core_controls:
            self._controls[cid] = SecurityControlRegistryDTO(
                control_id=cid,
                name=name,
                category=cat,  # type: ignore
                description=desc,
                status="ACTIVE",
                criticality="CRITICAL",
                verification_state="VERIFIED",
                last_verified=datetime.now(timezone.utc).isoformat(),
                evidence_count=3,
                version=1,
                freshness="CURRENT",
            )

    def register_control(
        self,
        name: str,
        category: ControlCategoryLiteral,
        description: str,
        criticality: str = "HIGH",
        tenant_id: str = "PLATFORM_SCOPE",
    ) -> SecurityControlRegistryDTO:
        """Registers a new security control into the catalog."""
        cid = f"ctrl_{uuid.uuid4().hex[:8]}"
        control = SecurityControlRegistryDTO(
            control_id=cid,
            tenant_id=tenant_id,
            name=name,
            category=category,
            description=description,
            status="REGISTERED",
            criticality=criticality,  # type: ignore
            verification_state="DOCUMENTED",
            last_verified=None,
            evidence_count=0,
            version=1,
            freshness="NEVER_TESTED",
        )
        self._controls[cid] = control
        return control

    def update_verification_state(
        self,
        control_id: str,
        state: VerificationStateLiteral,
        status: ControlLifecycleLiteral = "ACTIVE",
    ) -> SecurityControlRegistryDTO:
        """Updates control verification state following empirical test execution."""
        ctrl = self._controls.get(control_id)
        if not ctrl:
            raise KeyError(f"Control '{control_id}' not found.")

        ctrl.verification_state = state
        ctrl.status = status
        ctrl.last_verified = datetime.now(timezone.utc).isoformat()
        ctrl.evidence_count += 1
        ctrl.version += 1
        ctrl.freshness = "CURRENT" if state == "VERIFIED" else ctrl.freshness
        return ctrl

    def get_control(self, control_id: str, tenant_id: str = "PLATFORM_SCOPE") -> Optional[SecurityControlRegistryDTO]:
        """Retrieves control ensuring multi-tenant or platform scope matching."""
        ctrl = self._controls.get(control_id)
        if ctrl and (ctrl.tenant_id == tenant_id or ctrl.tenant_id == "PLATFORM_SCOPE"):
            return ctrl
        return None

    def list_controls(self, tenant_id: str = "PLATFORM_SCOPE") -> List[SecurityControlRegistryDTO]:
        """Lists controls visible to the requesting tenant."""
        return [c for c in self._controls.values() if c.tenant_id in (tenant_id, "PLATFORM_SCOPE")]
