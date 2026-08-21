"""Rollback Engine (Phase 4.0 Part 7 — Section 46).

Orchestrates action rollbacks and reports explicit ROLLBACK_UNAVAILABLE when the provider does not support reversal.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    ResponseActionDTO,
    ResponseRollbackDTO,
)
from app.services.soc.response_adapters import ResponseProviderAdapter, DNSResponseAdapter


class RollbackEngine:
    """Manages rollback lifecycle for completed or faulty security actions."""

    def __init__(self, adapters: Optional[Dict[str, ResponseProviderAdapter]] = None):
        self._adapters = adapters or {}

    def execute_rollback(
        self,
        action: ResponseActionDTO,
        executed_by: str = "SOC_LEAD",
        adapter: Optional[ResponseProviderAdapter] = None,
    ) -> Tuple[ResponseActionDTO, ResponseRollbackDTO]:
        provider = adapter or self._adapters.get(action.action_type, DNSResponseAdapter())

        success, reason = provider.rollback(action)

        if not success:
            # Section 46, Mandatory Test 8, 36: Explicitly report failure/unavailability
            status_val = "ROLLBACK_UNAVAILABLE" if "UNAVAILABLE" in reason else "ROLLBACK_FAILED"
            rollback_dto = ResponseRollbackDTO(
                action_id=action.action_id,
                target=action.target,
                rollback_status=status_val,
                reason=reason,
                executed_by=executed_by,
                error_message=reason,
            )
            action.status = status_val
            return action, rollback_dto

        # Successful rollback
        action.status = "ROLLED_BACK"
        rollback_dto = ResponseRollbackDTO(
            action_id=action.action_id,
            target=action.target,
            rollback_status="ROLLED_BACK",
            reason=reason,
            executed_by=executed_by,
        )
        return action, rollback_dto
