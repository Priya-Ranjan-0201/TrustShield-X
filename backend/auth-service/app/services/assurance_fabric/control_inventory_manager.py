"""
TruthShield X — Security Control Inventory Manager (Phase 24).

Manages the catalog of security controls across 20 functional categories with explicit expected/failure behaviors.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_assurance_fabric_models import SecurityControlDTO


class ControlInventoryManager:
    """Manages active, planned, and deprecated security controls."""

    def __init__(self):
        self._controls: Dict[str, SecurityControlDTO] = {}
        self._seed_default_controls()

    def _seed_default_controls(self):
        c1 = SecurityControlDTO(
            control_id="ctl_tenant_isolation",
            tenant_id="default_tenant",
            name="Strict Datastore Multi-Tenant Boundary",
            category="TENANT_ISOLATION",
            owner="usr_platform_sec",
            criticality="CRITICAL",
            implementation_status="IMPLEMENTED",
            validation_status="PASS",
            expected_behavior="Cross-tenant queries return empty set or raise PermissionDenied.",
            failure_behavior="Cross-tenant leakage occurs.",
            last_validated=datetime.now(timezone.utc).isoformat(),
            dependencies=["ast_pg_primary"],
        )
        c2 = SecurityControlDTO(
            control_id="ctl_four_eyes_response",
            tenant_id="default_tenant",
            name="Four-Eyes Governance for High-Impact SOAR Actions",
            category="SOAR",
            owner="usr_ciso",
            criticality="CRITICAL",
            implementation_status="IMPLEMENTED",
            validation_status="PASS",
            expected_behavior="High-impact actions require two distinct authorized principals.",
            failure_behavior="Single-user execution succeeds for high-impact action.",
            last_validated=datetime.now(timezone.utc).isoformat(),
            dependencies=["ast_api_gateway"],
        )
        c3 = SecurityControlDTO(
            control_id="ctl_immutable_audit",
            tenant_id="default_tenant",
            name="Immutable SHA-256 Audit Log Chaining",
            category="AUDIT",
            owner="usr_compliance_lead",
            criticality="HIGH",
            implementation_status="IMPLEMENTED",
            validation_status="PASS",
            expected_behavior="Audit log tamper attempts fail cryptographic hash chain verification.",
            failure_behavior="Audit record mutation succeeds without hash breach detection.",
            last_validated=datetime.now(timezone.utc).isoformat(),
            dependencies=["ast_pg_primary"],
        )
        for c in [c1, c2, c3]:
            self._controls[c.control_id] = c

    def register_control(self, control: SecurityControlDTO) -> SecurityControlDTO:
        self._controls[control.control_id] = control
        return control

    def get_control(self, control_id: str) -> Optional[SecurityControlDTO]:
        return self._controls.get(control_id)

    def list_controls(self, tenant_id: str = "default_tenant") -> List[SecurityControlDTO]:
        return [c for c in self._controls.values() if c.tenant_id == tenant_id or c.tenant_id == "default_tenant"]
