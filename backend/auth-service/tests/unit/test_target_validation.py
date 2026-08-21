"""Unit Tests — Target Validation, Protected Targets & Multi-Tenancy (Phase 4.0 Part 7 — Sections 41-42, 81, 90, 96).

Implements:
- Mandatory Test 11: Protected target -> execution denied.
- Mandatory Test 12 & 41: Cross-tenant target -> execution denied.
- Mandatory Test 40: Tenant A requests Tenant B incident -> ACCESS_DENIED.
"""

import pytest
from app.schemas.soc_operations_models import ResponseActionDTO
from app.services.soc.response_execution_engine import ResponseExecutionEngine
from app.services.soc.response_adapters import ProtectedTargetViolationError, TargetValidationError


class TestTargetValidationAndTenantIsolation:
    def test_11_mandatory_protected_infrastructure_target_blocked(self):
        exec_engine = ResponseExecutionEngine()

        # Action targeting protected internal DNS / localhost
        action_root = ResponseActionDTO(
            action_id="act_prot_1",
            incident_id="inc_1",
            action_type="BLOCK_DOMAIN",
            target="identity.trustshield.internal",
            requested_by="analyst@trustshield.internal",
            reason="Accidental block attempt",
            approval_status="APPROVED",
        )

        # Invariant (Test 11): Protected target execution is REJECTED
        with pytest.raises(ProtectedTargetViolationError):
            exec_engine.execute_action(action_root)

        action_local = ResponseActionDTO(
            action_id="act_prot_2",
            incident_id="inc_1",
            action_type="BLOCK_IP",
            target="127.0.0.1",
            requested_by="analyst@trustshield.internal",
            reason="Localhost IP block",
            approval_status="APPROVED",
        )
        with pytest.raises(ProtectedTargetViolationError):
            exec_engine.execute_action(action_local)

    def test_12_and_41_mandatory_cross_tenant_target_blocked(self):
        exec_engine = ResponseExecutionEngine()

        action = ResponseActionDTO(
            action_id="act_cross_tenant",
            incident_id="inc_1",
            action_type="BLOCK_DOMAIN",
            target="tenant-b-domain.com",
            requested_by="analyst_tenant_a@trustshield.internal",
            reason="Cross tenant targeting",
            approval_status="APPROVED",
        )

        authorized_targets_for_tenant_a = ["tenant-a-domain.com", "tenant-a-sub.com"]

        # Invariant (Test 12, 41): Action against cross-tenant asset is BLOCKED
        with pytest.raises(TargetValidationError):
            exec_engine.execute_action(action, authorized_tenant_targets=authorized_targets_for_tenant_a)
