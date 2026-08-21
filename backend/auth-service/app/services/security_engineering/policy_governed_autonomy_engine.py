"""
TruthShield X — Policy-Governed Autonomy Engine (Phase 25).

Enforces strict autonomy boundaries (Levels 0–4) and prevents automated bypass of required human gates.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import AutonomyGovernanceConfigDTO, AutonomyLevelLiteral


class PolicyGovernedAutonomyEngine:
    """Governs whether an action can execute autonomously or requires human approval."""

    def __init__(self):
        self._configs: Dict[str, AutonomyGovernanceConfigDTO] = {}
        self._seed_default_config()

    def _seed_default_config(self):
        cfg = AutonomyGovernanceConfigDTO(
            tenant_id="default_tenant",
            autonomy_level="LEVEL_3_CONTROLLED_AUTOMATION",
            allowed_actions=["TUNE_DETECTION_THRESHOLD", "OPTIMIZE_ALERT_CORRELATION", "UPDATE_AUDIT_FILTER"],
            prohibited_actions=["DISABLE_AUTH", "BYPASS_FOUR_EYES", "MUTATE_AUDIT_LOG", "WEAKEN_POLICY"],
            blast_radius_threshold=0.30,
        )
        self._configs[cfg.tenant_id] = cfg

    def can_auto_deploy(
        self,
        tenant_id: str,
        action_name: str,
        blast_radius: float,
        requires_human_approval: bool,
    ) -> bool:
        cfg = self._configs.get(tenant_id, self._configs["default_tenant"])

        # Invariant: If human approval is explicitly required, block auto deployment
        if requires_human_approval:
            return False

        # Invariant: Prohibited actions are never auto-deployed
        if action_name in cfg.prohibited_actions:
            return False

        # Invariant: Blast radius exceeding threshold requires human approval
        if blast_radius > cfg.blast_radius_threshold:
            return False

        # Autonomy Level Check
        if cfg.autonomy_level in ["LEVEL_3_CONTROLLED_AUTOMATION", "LEVEL_4_CONTINUOUSLY_VERIFIED_AUTOMATION"]:
            return action_name in cfg.allowed_actions

        return False

    def get_config(self, tenant_id: str = "default_tenant") -> AutonomyGovernanceConfigDTO:
        return self._configs.get(tenant_id, self._configs["default_tenant"])
