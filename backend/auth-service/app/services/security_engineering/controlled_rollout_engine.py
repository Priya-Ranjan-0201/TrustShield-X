"""
TruthShield X — Controlled Rollout Engine (Phase 25).

Orchestrates staged deployments (ISOLATED -> CANARY -> LIMITED -> FULL) with state capture for rollback.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import DeploymentRolloutDTO, RolloutStrategyLiteral


class ControlledRolloutEngine:
    """Manages staged rollouts and retains immutable previous states."""

    def __init__(self):
        self._deployments: Dict[str, DeploymentRolloutDTO] = {}

    def deploy_change(
        self,
        improvement_id: str,
        strategy: RolloutStrategyLiteral = "CANARY",
        previous_state: Optional[Dict[str, Any]] = None,
        new_state: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default_tenant",
    ) -> DeploymentRolloutDTO:
        dto = DeploymentRolloutDTO(
            improvement_id=improvement_id,
            tenant_id=tenant_id,
            strategy=strategy,
            previous_state=previous_state or {"rule_active": False},
            new_state=new_state or {"rule_active": True, "scope": "canary_10pct"},
            deployed_at=datetime.now(timezone.utc).isoformat(),
            status="CANARY_ACTIVE" if strategy == "CANARY" else "DEPLOYED_FULL",
        )
        self._deployments[dto.deployment_id] = dto
        return dto

    def get_deployment(self, deployment_id: str) -> Optional[DeploymentRolloutDTO]:
        return self._deployments.get(deployment_id)
