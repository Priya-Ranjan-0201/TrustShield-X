"""Autonomous Cyber Defense & Digital Trust Orchestrator (Phase 5).

Implements the unified core loop:
DETECT → CORRELATE → UNDERSTAND → ASSESS RISK → DECIDE → AUTHORIZE → SIMULATE → EXECUTE → VERIFY → AUDIT → LEARN
"""

from typing import List, Dict, Any, Optional, Tuple
import hashlib
import json
import uuid
import time
from datetime import datetime, timezone

from app.schemas.autonomous_defense_models import (
    ResponsePlanDTO,
    ResponsePlanActionDTO,
    DecisionContextDTO,
    DecisionResultDTO,
    SimulationResultDTO,
    VerificationResultDTO,
    RollbackResultDTO,
    EffectivenessScoreDTO,
    ExecutionStateLiteral,
)
from app.schemas.soc_operations_models import (
    ResponseActionDTO,
    ApprovalStatusLiteral,
)
from app.services.response_decision_engine import ResponseDecisionEngine
from app.services.protected_target_engine import ProtectedTargetEngine, ProtectedTargetViolationError, TargetValidationError
from app.services.response_effectiveness_engine import ResponseEffectivenessEngine
from app.services.soc.approval_engine import ApprovalEngine, ApprovalPolicyViolationError
from app.services.soc.response_adapters import (
    ResponseProviderAdapter,
    DNSResponseAdapter,
    FirewallResponseAdapter,
    EDRResponseAdapter,
    UnknownExecutionStateError,
)
from app.services.soc.response_adapters.extended_adapters import (
    IAMResponseAdapter,
    FraudControlResponseAdapter,
    CloudStorageResponseAdapter,
)


class AutonomousDefenseOrchestrator:
    """Flagship operational defense orchestrator for TruthShield X."""

    def __init__(
        self,
        decision_engine: Optional[ResponseDecisionEngine] = None,
        approval_engine: Optional[ApprovalEngine] = None,
        effectiveness_engine: Optional[ResponseEffectivenessEngine] = None,
        adapters: Optional[Dict[str, ResponseProviderAdapter]] = None,
    ):
        self.decision_engine = decision_engine or ResponseDecisionEngine()
        self.approval_engine = approval_engine or ApprovalEngine()
        self.effectiveness_engine = effectiveness_engine or ResponseEffectivenessEngine()
        self._plans: Dict[str, ResponsePlanDTO] = {}
        self._completed_idempotency: Dict[str, ResponsePlanActionDTO] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self._last_audit_hash: str = "0" * 64

        # Register Multi-Vendor Adapters
        self._adapters: Dict[str, ResponseProviderAdapter] = adapters or {
            "BLOCK_DOMAIN": DNSResponseAdapter(),
            "BLOCK_IP": FirewallResponseAdapter(),
            "QUARANTINE_FILE": EDRResponseAdapter(),
            "ISOLATE_DEVICE": EDRResponseAdapter(),
            "DISABLE_ACCOUNT": IAMResponseAdapter(),
            "REVOKE_TOKEN": IAMResponseAdapter(),
            "REVOKE_SESSION": IAMResponseAdapter(),
            "RESET_CREDENTIAL": IAMResponseAdapter(),
            "FREEZE_UPI_HANDLE": FraudControlResponseAdapter(),
            "ISOLATE_S3_BUCKET": CloudStorageResponseAdapter(),
        }

    def _append_audit_event(self, action: str, tenant_id: str, payload: Dict[str, Any]) -> str:
        """Appends tamper-evident SHA-256 chained audit record."""
        payload_str = json.dumps(payload, sort_keys=True)
        new_hash = hashlib.sha256((self._last_audit_hash + payload_str).encode()).hexdigest()
        event = {
            "action": action,
            "tenant_id": tenant_id,
            "previous_hash": self._last_audit_hash,
            "current_hash": new_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        self._audit_log.append(event)
        self._last_audit_hash = new_hash
        return new_hash

    def create_response_plan(
        self,
        tenant_id: str,
        incident_id: str,
        title: str,
        description: str,
        threat_contexts: List[DecisionContextDTO],
        campaign_id: Optional[str] = None,
    ) -> ResponsePlanDTO:
        """Generates an immutable response plan from evaluated threat contexts."""
        actions: List[ResponsePlanActionDTO] = []
        requires_approval = False
        highest_risk = 0.0
        avg_confidence = 1.0

        for ctx in threat_contexts:
            ctx.tenant_id = tenant_id
            decision_res = self.decision_engine.evaluate_decision(ctx)
            highest_risk = max(highest_risk, ctx.risk_score)
            avg_confidence = min(avg_confidence, ctx.confidence)

            if decision_res.required_approval:
                requires_approval = True

            action = ResponsePlanActionDTO(
                action_type=decision_res.recommended_action,
                target=decision_res.target or ctx.target,
                target_type=ctx.target_type,
                safety_classification=decision_res.safety_classification,
                risk_level=ctx.severity,
                approval_required=decision_res.required_approval,
                approval_status="PENDING" if decision_res.required_approval else "NOT_REQUIRED",
                state="CREATED",
                dry_run_supported=True,
                rollback_supported=decision_res.safety_classification not in ("IRREVERSIBLE",),
            )
            actions.append(action)

        plan = ResponsePlanDTO(
            tenant_id=tenant_id,
            incident_id=incident_id,
            campaign_id=campaign_id,
            title=title,
            description=description,
            risk_score=highest_risk,
            confidence=avg_confidence,
            actions=actions,
            state="CREATED",
            requires_human_approval=requires_approval,
            all_approved=not requires_approval,
            rollback_plan=[f"Rollback {a.action_type} on {a.target}" for a in actions if a.rollback_supported],
            verification_plan=[f"Verify state of {a.target} via provider probe" for a in actions],
            expected_outcome=f"Contain threat with residual risk < 15.0 for incident {incident_id}",
        )

        # Hash immutable content
        content_bytes = json.dumps(plan.model_dump(exclude={"content_hash"}), sort_keys=True).encode()
        plan.content_hash = hashlib.sha256(content_bytes).hexdigest()

        self._plans[plan.plan_id] = plan
        self._append_audit_event("PLAN_CREATED", tenant_id, {"plan_id": plan.plan_id, "content_hash": plan.content_hash})
        return plan

    def simulate_plan(self, plan_id: str, tenant_id: str) -> SimulationResultDTO:
        """Performs zero-mutation dry-run simulation of response plan."""
        plan = self._plans.get(plan_id)
        if not plan or plan.tenant_id != tenant_id:
            raise KeyError(f"Response plan '{plan_id}' not found for tenant '{tenant_id}'.")

        side_effects: List[str] = []
        for a in plan.actions:
            # Check protected targets during simulation
            ProtectedTargetEngine.validate_action_target(a.target, a.target_type, tenant_id)
            adapter = self._adapters.get(a.action_type, DNSResponseAdapter())
            mock_action = ResponseActionDTO(
                action_id=a.action_id,
                incident_id=plan.incident_id or "inc_sim",
                action_type=a.action_type,
                target=a.target,
                target_type=a.target_type,
                requested_by="SIMULATION_ENGINE",
                reason="Dry-run preview",
            )
            sim_res = adapter.dry_run(mock_action)
            side_effects.append(f"{a.action_type} on {a.target}: {sim_res.get('status', 'OK')}")

        plan.state = "SIMULATED"
        sim = SimulationResultDTO(
            plan_id=plan_id,
            simulated_actions_count=len(plan.actions),
            mutations_expected=0,
            external_network_calls_blocked=len(plan.actions),
            policy_evaluation_passed=True,
            side_effects=side_effects,
            verdict="SIMULATION_PASSED_ZERO_EXTERNAL_MUTATION",
        )
        self._append_audit_event("PLAN_SIMULATED", tenant_id, {"plan_id": plan_id, "simulation_id": sim.simulation_id})
        return sim

    def request_action_approval(
        self,
        plan_id: str,
        action_id: str,
        requested_by: str,
        reason: str,
        tenant_id: str,
    ) -> str:
        """Submits an action for four-eyes authorization."""
        plan = self._plans.get(plan_id)
        if not plan or plan.tenant_id != tenant_id:
            raise KeyError(f"Plan {plan_id} not found.")

        target_action = next((a for a in plan.actions if a.action_id == action_id), None)
        if not target_action:
            raise KeyError(f"Action {action_id} not in plan.")

        mock_soc_act = ResponseActionDTO(
            action_id=target_action.action_id,
            incident_id=plan.incident_id or "inc_default",
            action_type=target_action.action_type,
            target=target_action.target,
            target_type=target_action.target_type,
            requested_by=requested_by,
            reason=reason,
        )
        appr_dto = self.approval_engine.create_approval_request(
            action=mock_soc_act,
            requested_by=requested_by,
            reason=reason,
            risk=target_action.risk_level,
        )
        target_action.approval_id = appr_dto.approval_id
        target_action.state = "AWAITING_APPROVAL"
        plan.state = "AWAITING_APPROVAL"

        self._append_audit_event("APPROVAL_REQUESTED", tenant_id, {
            "plan_id": plan_id,
            "action_id": action_id,
            "approval_id": appr_dto.approval_id,
            "requested_by": requested_by,
        })
        return appr_dto.approval_id

    def approve_action(
        self,
        approval_id: str,
        approver_id: str,
        decision: ApprovalStatusLiteral,
        decision_reason: str,
        tenant_id: str,
    ) -> bool:
        """Applies four-eyes approval decision with separation of duties enforcement."""
        appr_dto = self.approval_engine.decide_approval(
            approval_id=approval_id,
            approver_id=approver_id,
            decision=decision,
            decision_reason=decision_reason,
            enforce_separation_of_duties=True,
        )

        # Update action state in plan
        for plan in self._plans.values():
            if plan.tenant_id == tenant_id:
                for a in plan.actions:
                    if a.approval_id == approval_id:
                        a.approval_status = decision
                        if decision == "APPROVED":
                            a.state = "APPROVED"
                        else:
                            a.state = "CANCELLED"

                # Check if all actions approved
                if all(act.approval_status in ("APPROVED", "NOT_REQUIRED") for act in plan.actions):
                    plan.all_approved = True
                    plan.state = "APPROVED"

        self._append_audit_event("APPROVAL_DECIDED", tenant_id, {
            "approval_id": approval_id,
            "approver_id": approver_id,
            "decision": decision,
        })
        return decision == "APPROVED"

    def execute_plan(
        self,
        plan_id: str,
        tenant_id: str,
        authorized_tenant_targets: Optional[List[str]] = None,
    ) -> List[ResponsePlanActionDTO]:
        """Executes all approved actions in a plan with unknown-state handling and idempotency."""
        plan = self._plans.get(plan_id)
        if not plan or plan.tenant_id != tenant_id:
            raise KeyError(f"Plan {plan_id} not found.")

        plan.state = "EXECUTING"
        executed_actions: List[ResponsePlanActionDTO] = []

        for action in plan.actions:
            # 1. Protected Target Check (Section 10, SSRF / Loopback guard)
            ProtectedTargetEngine.validate_action_target(
                action.target,
                action.target_type,
                tenant_id,
                authorized_tenant_targets,
            )

            # 2. Authorization Verification
            if action.approval_required and action.approval_status != "APPROVED":
                action.state = "AWAITING_APPROVAL"
                continue

            # 3. Idempotency Check
            if action.idempotency_key in self._completed_idempotency:
                existing = self._completed_idempotency[action.idempotency_key]
                executed_actions.append(existing)
                continue

            adapter = self._adapters.get(action.action_type, DNSResponseAdapter())
            mock_action = ResponseActionDTO(
                action_id=action.action_id,
                incident_id=plan.incident_id or "inc_default",
                action_type=action.action_type,
                target=action.target,
                target_type=action.target_type,
                requested_by="AUTONOMOUS_DEFENSE_ENGINE",
                reason="Plan execution",
                approval_status=action.approval_status,
                idempotency_key=action.idempotency_key,
            )

            action.started_at = datetime.now(timezone.utc).isoformat()
            action.state = "EXECUTING"

            try:
                res = adapter.execute(mock_action)
                action.state = "EXECUTED"
                action.completed_at = datetime.now(timezone.utc).isoformat()
                action.result_summary = str(res.get("message", "Success"))
                self._completed_idempotency[action.idempotency_key] = action
                executed_actions.append(action)

            except UnknownExecutionStateError as ue:
                # Critical Invariant: Provider timeout -> EXECUTION_UNKNOWN (No blind retries)
                action.state = "EXECUTION_UNKNOWN"
                action.error_message = str(ue)
                executed_actions.append(action)

            except Exception as ex:
                action.state = "FAILED"
                action.error_message = str(ex)
                executed_actions.append(action)

        # Update overall plan state
        if any(a.state == "EXECUTION_UNKNOWN" for a in plan.actions):
            plan.state = "EXECUTION_UNKNOWN"
        elif all(a.state == "EXECUTED" for a in plan.actions):
            plan.state = "EXECUTED"
        elif any(a.state == "FAILED" for a in plan.actions):
            plan.state = "FAILED"

        self._append_audit_event("PLAN_EXECUTED", tenant_id, {
            "plan_id": plan_id,
            "plan_state": plan.state,
            "executed_count": len(executed_actions),
        })
        return executed_actions

    def verify_plan(self, plan_id: str, tenant_id: str) -> List[VerificationResultDTO]:
        """Queries provider actual state post-execution to verify containment."""
        plan = self._plans.get(plan_id)
        if not plan or plan.tenant_id != tenant_id:
            raise KeyError(f"Plan {plan_id} not found.")

        plan.state = "VERIFYING"
        verifications: List[VerificationResultDTO] = []

        for action in plan.actions:
            if action.state in ("EXECUTED", "EXECUTION_UNKNOWN"):
                adapter = self._adapters.get(action.action_type, DNSResponseAdapter())
                mock_action = ResponseActionDTO(
                    action_id=action.action_id,
                    incident_id=plan.incident_id or "inc_default",
                    action_type=action.action_type,
                    target=action.target,
                    requested_by="AUTONOMOUS_DEFENSE_ENGINE",
                    reason="Post-execution containment verification",
                )
                t0 = time.time()
                status, obs = adapter.verify(mock_action)
                latency = (time.time() - t0) * 1000.0

                passed = (status == "SUCCESS")
                action.state = "VERIFIED" if passed else "FAILED"
                action.verified_at = datetime.now(timezone.utc).isoformat()

                ver_dto = VerificationResultDTO(
                    action_id=action.action_id,
                    target=action.target,
                    verified_state="CONTAINED" if passed else "ACTIVE",
                    empirical_evidence=[obs],
                    verification_passed=passed,
                    latency_ms=round(latency, 2),
                )
                verifications.append(ver_dto)

        if all(v.verification_passed for v in verifications):
            plan.state = "VERIFIED"
        else:
            plan.state = "FAILED"

        self._append_audit_event("PLAN_VERIFIED", tenant_id, {
            "plan_id": plan_id,
            "all_passed": all(v.verification_passed for v in verifications),
        })
        return verifications

    def rollback_action(self, plan_id: str, action_id: str, tenant_id: str, executed_by: str = "SOC_LEAD") -> RollbackResultDTO:
        """Reverts an executed action where supported."""
        plan = self._plans.get(plan_id)
        if not plan or plan.tenant_id != tenant_id:
            raise KeyError(f"Plan {plan_id} not found.")

        action = next((a for a in plan.actions if a.action_id == action_id), None)
        if not action:
            raise KeyError(f"Action {action_id} not found.")

        adapter = self._adapters.get(action.action_type, DNSResponseAdapter())
        mock_action = ResponseActionDTO(
            action_id=action.action_id,
            incident_id=plan.incident_id or "inc_default",
            action_type=action.action_type,
            target=action.target,
            requested_by=executed_by,
            reason="Remediation rollback request",
        )
        success, reason = adapter.rollback(mock_action)

        status_val = "ROLLED_BACK" if success else ("ROLLBACK_UNAVAILABLE" if "UNAVAILABLE" in reason else "ROLLBACK_FAILED")
        action.state = status_val

        rol_dto = RollbackResultDTO(
            action_id=action.action_id,
            target=action.target,
            rollback_status=status_val,
            reason=reason,
            executed_by=executed_by,
        )

        self._append_audit_event("ACTION_ROLLED_BACK", tenant_id, {
            "plan_id": plan_id,
            "action_id": action_id,
            "status": status_val,
        })
        return rol_dto

    def get_plan(self, plan_id: str, tenant_id: str) -> Optional[ResponsePlanDTO]:
        plan = self._plans.get(plan_id)
        if plan and plan.tenant_id == tenant_id:
            return plan
        return None

    def list_plans(self, tenant_id: str) -> List[ResponsePlanDTO]:
        return [p for p in self._plans.values() if p.tenant_id == tenant_id]

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return list(self._audit_log)
