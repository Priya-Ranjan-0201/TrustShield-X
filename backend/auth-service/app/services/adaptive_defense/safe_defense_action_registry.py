"""
TruthShield X — Safe Defense Action Registry & Protected Targets (Phase 17).

Catalog of pre-authorized actions, automation level mappings, and protected target validation.
"""

from typing import Dict, List, Optional
from app.schemas.adaptive_defense_models import (
    SafeDefenseActionDefinitionDTO,
    ActionClassificationLiteral,
    AutomationLevelLiteral,
)


class ProtectedTargetViolationError(Exception):
    """Raised when an action targets protected core infrastructure."""
    pass


PROTECTED_TARGETS = {
    "127.0.0.1",
    "localhost",
    "10.0.0.1",
    "192.168.1.1",
    "trustshield.internal",
    "identity.trustshield.internal",
    "root",
    "admin",
    "production-db-primary",
    "aws-root-account",
    "k8s-control-plane",
}


class SafeDefenseActionRegistry:
    """Registry of pre-authorized defense action definitions and target safeguards."""

    def __init__(self):
        self._actions: Dict[str, SafeDefenseActionDefinitionDTO] = {}
        self._initialize_default_catalog()

    def _initialize_default_catalog(self):
        defaults = [
            SafeDefenseActionDefinitionDTO(
                action_type="INCREASE_LOGGING",
                description="Increases telemetry and audit logging verbosity on endpoint",
                scope="ENDPOINT",
                allowed_target_patterns=["srv-*", "host-*", "ep-*"],
                requires_approval=False,
                owner_team="SOC_AUTOMATION",
            ),
            SafeDefenseActionDefinitionDTO(
                action_type="BLOCK_EXTERNAL_IP",
                description="Adds temporary edge firewall drop rule for malicious IP",
                scope="NETWORK_BOUNDARY",
                allowed_target_patterns=["*"],
                requires_approval=False,
                owner_team="NETWORK_SECURITY",
            ),
            SafeDefenseActionDefinitionDTO(
                action_type="ISOLATE_HOST",
                description="Quarantines host from corporate network into isolated VLAN",
                scope="ENDPOINT",
                allowed_target_patterns=["ep-*", "workstation-*"],
                requires_approval=True,  # Level 2 Human Approval
                owner_team="INCIDENT_RESPONSE",
            ),
            SafeDefenseActionDefinitionDTO(
                action_type="FORCE_STEP_UP_MFA",
                description="Enforces MFA challenge on next authentication attempt",
                scope="IDENTITY",
                allowed_target_patterns=["usr_*", "svc_*"],
                requires_approval=False,
                owner_team="IAM_TEAM",
            ),
        ]
        for a in defaults:
            self._actions[a.action_type] = a

    def get_action_definition(self, action_type: str) -> Optional[SafeDefenseActionDefinitionDTO]:
        return self._actions.get(action_type)

    def validate_target_safety(self, target: str) -> bool:
        """Validates that a target is not in the protected target blacklist."""
        t_clean = target.strip().lower()
        if t_clean in PROTECTED_TARGETS or any(p in t_clean for p in ("trustshield.internal", "aws-root")):
            raise ProtectedTargetViolationError(
                f"Action blocked: Target '{target}' is protected infrastructure."
            )
        return True

    def list_actions(self) -> List[SafeDefenseActionDefinitionDTO]:
        return list(self._actions.values())
