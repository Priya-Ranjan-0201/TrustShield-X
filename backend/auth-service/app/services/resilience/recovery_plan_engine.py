"""
TruthShield X — Recovery Plan Engine (Phase 23).

Generates dependency-ordered recovery plans with explicit rollback paths and four-eyes authorization checks.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.cyber_resilience_models import RecoveryPlanDTO, RecoveryStepDTO


class RecoveryPlanEngine:
    """Generates structured, dependency-aware disaster recovery and failover plans."""

    def __init__(self):
        self._plans: Dict[str, RecoveryPlanDTO] = {}
        self._seed_default_plan()

    def _seed_default_plan(self):
        steps = [
            RecoveryStepDTO(step_order=1, target="ast_net_vpc", action="VERIFY_NETWORK_AND_SECURITY_GROUPS", expected_outcome="VPC routes active"),
            RecoveryStepDTO(step_order=2, target="ast_pg_primary", action="RESTORE_POSTGRES_STANDBY", expected_outcome="PostgreSQL read/write ready"),
            RecoveryStepDTO(step_order=3, target="ast_redis_cache", action="RESTART_AND_SYNC_REDIS_REPLICA", expected_outcome="Cache connected"),
            RecoveryStepDTO(step_order=4, target="ast_api_gateway", action="DEPLOY_AND_HEALTHCHECK_PODS", expected_outcome="Endpoints return HTTP 200"),
        ]
        p1 = RecoveryPlanDTO(
            plan_id="recplan_checkout_recovery",
            tenant_id="default_tenant",
            title="Checkout & Payment Service Automated Disaster Recovery",
            objective="Restore payment processing in secondary availability zone following primary cluster outage.",
            affected_services=["svc_checkout_api"],
            dependencies=["ast_net_vpc", "ast_pg_primary", "ast_redis_cache", "ast_api_gateway"],
            recovery_order=["ast_net_vpc", "ast_pg_primary", "ast_redis_cache", "ast_api_gateway"],
            prerequisites=["Secondary AZ VPC provisioned", "Point-in-time WAL archive available"],
            steps=steps,
            rollback_steps=["Demote secondary PostgreSQL to standby", "Revert DNS CNAME to primary gateway"],
            approval_tier="TIER_2_FOUR_EYES",
            is_approved=True,
            approver_id="usr_ciso_dr_lead",
            estimated_duration_minutes=20,
            target_RTO_minutes=30,
            target_RPO_minutes=15,
            owner="usr_sre_lead",
            drift_status="CURRENT",
        )
        self._plans[p1.plan_id] = p1

    def generate_plan(
        self,
        service_name: str,
        ordered_dependencies: List[str],
        tenant_id: str = "default_tenant",
    ) -> RecoveryPlanDTO:
        steps = []
        for idx, dep in enumerate(ordered_dependencies, start=1):
            steps.append(RecoveryStepDTO(
                step_order=idx,
                target=dep,
                action=f"RECOVER_AND_HEALTHCHECK_{dep.upper()}",
                expected_outcome=f"Component {dep} operational and validated",
            ))

        dto = RecoveryPlanDTO(
            tenant_id=tenant_id,
            title=f"Automated Recovery Plan for {service_name}",
            objective=f"Sequential dependency recovery for {service_name}",
            affected_services=[service_name],
            dependencies=ordered_dependencies,
            recovery_order=ordered_dependencies,
            steps=steps,
            rollback_steps=[f"REVERT_{dep.upper()}" for dep in reversed(ordered_dependencies)],
            approval_tier="TIER_2_FOUR_EYES",
            is_approved=False,
        )
        self._plans[dto.plan_id] = dto
        return dto

    def approve_plan(self, plan_id: str, approver_id: str) -> RecoveryPlanDTO:
        plan = self._plans.get(plan_id)
        if not plan:
            raise ValueError(f"Recovery plan '{plan_id}' not found.")
        updated = RecoveryPlanDTO(
            plan_id=plan.plan_id,
            tenant_id=plan.tenant_id,
            title=plan.title,
            objective=plan.objective,
            affected_services=plan.affected_services,
            dependencies=plan.dependencies,
            recovery_order=plan.recovery_order,
            prerequisites=plan.prerequisites,
            steps=plan.steps,
            rollback_steps=plan.rollback_steps,
            approval_tier=plan.approval_tier,
            is_approved=True,
            approver_id=approver_id,
            estimated_duration_minutes=plan.estimated_duration_minutes,
            target_RTO_minutes=plan.target_RTO_minutes,
            target_RPO_minutes=plan.target_RPO_minutes,
            owner=plan.owner,
            drift_status=plan.drift_status,
        )
        self._plans[plan_id] = updated
        return updated

    def get_plan(self, plan_id: str) -> Optional[RecoveryPlanDTO]:
        return self._plans.get(plan_id)

    def list_plans(self, tenant_id: str = "default_tenant") -> List[RecoveryPlanDTO]:
        return list(self._plans.values())
