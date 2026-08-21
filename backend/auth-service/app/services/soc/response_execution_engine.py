"""Response Execution Engine, Protected Targets & Idempotency (Phase 4.0 Part 7 — Sections 39-45).

Coordinates safe remediation execution with strict target validation, protected target checks,
approval verification, and idempotency guarantees.
"""

from typing import List, Dict, Any, Optional, Tuple
import time
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    ResponseActionDTO,
    ResponseExecutionDTO,
    ExecutionStatusLiteral,
)
from app.services.soc.response_adapters import (
    ResponseProviderAdapter,
    DNSResponseAdapter,
    FirewallResponseAdapter,
    EDRResponseAdapter,
    TargetValidationError,
    ProtectedTargetViolationError,
    UnknownExecutionStateError,
)

PROTECTED_TARGETS = {
    "127.0.0.1",
    "localhost",
    "10.0.0.1",
    "192.168.1.1",
    "trustshield.internal",
    "identity.trustshield.internal",
    "root",
    "admin",
    "soc_lead",
    "auth-service",
}


class ResponseExecutionEngine:
    """Safely dispatches approved actions to provider adapters."""

    def __init__(self, adapters: Optional[Dict[str, ResponseProviderAdapter]] = None):
        self._executions: Dict[str, ResponseExecutionDTO] = {}
        self._completed_idempotency_keys: Dict[str, ResponseActionDTO] = {}
        self._adapters: Dict[str, ResponseProviderAdapter] = adapters if adapters is not None else {
            "BLOCK_DOMAIN": DNSResponseAdapter(),
            "BLOCK_IP": FirewallResponseAdapter(),
            "QUARANTINE_FILE": EDRResponseAdapter(),
            "ISOLATE_DEVICE": EDRResponseAdapter(),
        }

    def register_adapter(self, action_type: str, adapter: ResponseProviderAdapter) -> None:
        self._adapters[action_type] = adapter

    def validate_action_target(self, action: ResponseActionDTO, authorized_tenant_targets: Optional[List[str]] = None) -> None:
        """Validate target presence, tenant ownership, and protected infrastructure status (Section 41-42)."""
        target = action.target.strip().lower()

        # 1. Protected Target Check (Section 42, Mandatory Test 11)
        if target in PROTECTED_TARGETS or any(p in target for p in ("trustshield.internal", "aws-root-account")):
            raise ProtectedTargetViolationError(
                f"Action '{action.action_type}' rejected: Target '{action.target}' is protected infrastructure."
            )

        # 2. Multi-Tenant Target Scope Check (Section 41, Mandatory Test 12)
        if authorized_tenant_targets is not None and target not in [t.lower() for t in authorized_tenant_targets]:
            raise TargetValidationError(
                f"Target '{action.target}' does not belong to the authorized tenant context."
            )

    def execute_action(
        self,
        action: ResponseActionDTO,
        authorized_tenant_targets: Optional[List[str]] = None,
        bypass_approval_for_test: bool = False,
    ) -> Tuple[ResponseActionDTO, ResponseExecutionDTO]:
        """Execute action through registered adapter with safety checks."""
        # 1. Target Validation
        self.validate_action_target(action, authorized_tenant_targets)

        # 2. Approval Verification (Section 34, Mandatory Test 5)
        if not bypass_approval_for_test and action.approval_status != "APPROVED":
            action.status = "WAITING_APPROVAL"
            raise PermissionError(f"Action '{action.action_id}' is not approved. Current status: {action.approval_status}")

        # 3. Action Replay & Idempotency Check (Section 84, Mandatory Test 6)
        if action.idempotency_key in self._completed_idempotency_keys:
            existing = self._completed_idempotency_keys[action.idempotency_key]
            exec_rec = self._executions.get(existing.action_id)
            if exec_rec:
                return existing, exec_rec

        # 4. Resolve Adapter
        adapter = self._adapters.get(action.action_type, DNSResponseAdapter())
        now_str = datetime.now(timezone.utc).isoformat()
        action.started_at = now_str
        action.status = "EXECUTING"

        start_time = time.time()
        try:
            res = adapter.execute(action)
            exec_time = (time.time() - start_time) * 1000.0
            action.status = "VERIFYING"
            action.completed_at = datetime.now(timezone.utc).isoformat()
            action.result_reference = str(res.get("message", "Success"))

            execution = ResponseExecutionDTO(
                action_id=action.action_id,
                provider_name=adapter.__class__.__name__,
                status="COMPLETED",
                request_payload={"target": action.target, "action": action.action_type},
                response_payload=res,
                execution_time_ms=exec_time,
            )

            self._executions[action.action_id] = execution
            self._completed_idempotency_keys[action.idempotency_key] = action
            return action, execution

        except UnknownExecutionStateError as ue:
            # Section 48, Mandatory Test 7: Provider timed out after potentially executing
            action.status = "UNKNOWN_EXECUTION_STATE"
            action.error_code = "ERR_PROVIDER_TIMEOUT"
            execution = ResponseExecutionDTO(
                action_id=action.action_id,
                provider_name=adapter.__class__.__name__,
                status="UNKNOWN_EXECUTION_STATE",
                error_message=str(ue),
            )
            self._executions[action.action_id] = execution
            return action, execution

        except Exception as ex:
            action.status = "FAILED"
            action.error_code = "ERR_EXECUTION_FAILED"
            execution = ResponseExecutionDTO(
                action_id=action.action_id,
                provider_name=adapter.__class__.__name__,
                status="FAILED",
                error_message=str(ex),
            )
            self._executions[action.action_id] = execution
            return action, execution
