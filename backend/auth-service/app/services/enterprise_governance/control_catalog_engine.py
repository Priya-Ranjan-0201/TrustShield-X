"""
TruthShield X — Control Catalog Engine (Phase 32).

Maintains the authoritative catalog of enterprise security controls, tracking primary/backup owners,
lifecycle states, implementation maturity, and empirical effectiveness.
"""

from typing import Dict, List, Optional, Any
from app.schemas.enterprise_governance_models import ControlDTO, ControlStatusLiteral, ControlEffectivenessLiteral


class ControlCatalogEngine:
    """Enterprise security control catalog with zero-orphan ownership guarantees."""

    def __init__(self):
        self._controls: Dict[str, ControlDTO] = {}
        self._seed_default_controls()

    def _seed_default_controls(self):
        c1 = ControlDTO(
            control_id="ctrl_iam_mfa_enforcement",
            name="Universal Multi-Factor Authentication Enforcement",
            description="Mandates cryptographically backed MFA on all corporate and administrative sessions",
            primary_owner="IAM_LEAD",
            backup_owner="CISO_OPS",
            domain="IDENTITY_AND_ACCESS",
            implementation_status="VERIFIED",
            effectiveness="EFFECTIVE",
            risk_level="HIGH",
            tenant_id="default_tenant",
            status="ACTIVE",
        )
        c2 = ControlDTO(
            control_id="ctrl_data_encryption_at_rest",
            name="AES-256-GCM Storage Encryption",
            description="Enforces envelope encryption on all database volumes and object stores",
            primary_owner="CRYPTO_LEAD",
            backup_owner="INFRA_LEAD",
            domain="DATA_PROTECTION",
            implementation_status="VERIFIED",
            effectiveness="EFFECTIVE",
            risk_level="CRITICAL",
            tenant_id="default_tenant",
            status="ACTIVE",
        )
        self._controls[c1.control_id] = c1
        self._controls[c2.control_id] = c2

    def register_control(self, control: ControlDTO) -> ControlDTO:
        if not control.primary_owner or not control.backup_owner:
            raise ValueError("Every control must have a designated primary and backup owner (no orphan controls).")
        self._controls[control.control_id] = control
        return control

    def get_control(self, control_id: str) -> Optional[ControlDTO]:
        return self._controls.get(control_id)

    def list_controls(self, tenant_id: str = "default_tenant") -> List[ControlDTO]:
        return [c for c in self._controls.values() if c.tenant_id == tenant_id]
