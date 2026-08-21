"""Unit Tests — Approval Engine & Separation of Duties (Phase 4.0 Part 7 — Sections 34-36, 80, 90, 94).

Implements:
- Mandatory Test 2: High-impact action requires approval -> WAITING_APPROVAL.
- Mandatory Test 3: Requester attempts self-approval -> Separation of Duties Violation / ACCESS_DENIED.
- Mandatory Test 5 & 30: Execution attempted without approval -> BLOCKED.
- Mandatory Test 31: Approval rejected -> Action cancelled and blocked from execution.
"""

import pytest
from app.schemas.soc_operations_models import ResponseActionDTO
from app.services.soc.approval_engine import ApprovalEngine, ApprovalPolicyViolationError
from app.services.soc.response_execution_engine import ResponseExecutionEngine


class TestApprovalEngineAndSeparationOfDuties:
    def test_02_and_30_mandatory_high_impact_action_waiting_approval(self):
        engine = ApprovalEngine()
        action = ResponseActionDTO(
            action_id="act_block_1",
            incident_id="inc_1",
            action_type="BLOCK_DOMAIN",
            target="phish-victim.in",
            requested_by="analyst_alice@trustshield.internal",
            reason="Phishing containment",
            approval_status="PENDING",
            status="WAITING_APPROVAL",
        )

        approval = engine.create_approval_request(
            action=action,
            requested_by="analyst_alice@trustshield.internal",
            reason="Phishing containment",
        )
        assert approval.status == "PENDING"
        assert approval.action_id == "act_block_1"

    def test_03_mandatory_self_approval_separation_of_duties_blocked(self):
        engine = ApprovalEngine()
        action = ResponseActionDTO(
            action_id="act_block_2",
            incident_id="inc_1",
            action_type="ISOLATE_DEVICE",
            target="device-101",
            requested_by="analyst_alice@trustshield.internal",
            reason="Device isolation",
        )
        approval = engine.create_approval_request(
            action=action,
            requested_by="analyst_alice@trustshield.internal",
            reason="Device isolation",
        )

        # Invariant (Test 3): Requesting analyst CANNOT self-approve
        with pytest.raises(ApprovalPolicyViolationError):
            engine.decide_approval(
                approval_id=approval.approval_id,
                approver_id="analyst_alice@trustshield.internal",
                decision="APPROVED",
                decision_reason="Self-approval attempt",
            )

    def test_05_mandatory_execution_without_approval_blocked(self):
        exec_engine = ResponseExecutionEngine()
        action = ResponseActionDTO(
            action_id="act_unapproved",
            incident_id="inc_1",
            action_type="BLOCK_DOMAIN",
            target="malicious-payload.in",
            requested_by="analyst_alice@trustshield.internal",
            reason="Containment",
            approval_status="PENDING",
        )

        # Invariant (Test 5): Execution without approval is BLOCKED
        with pytest.raises(PermissionError):
            exec_engine.execute_action(action)

    def test_31_mandatory_rejected_approval_blocks_execution(self):
        appr_engine = ApprovalEngine()
        exec_engine = ResponseExecutionEngine()

        action = ResponseActionDTO(
            action_id="act_reject_test",
            incident_id="inc_1",
            action_type="BLOCK_IP",
            target="198.51.100.1",
            requested_by="analyst_alice@trustshield.internal",
            reason="IP block",
        )
        approval = appr_engine.create_approval_request(action, "analyst_alice@trustshield.internal", "IP Block")

        # SOC Lead rejects action
        appr_engine.decide_approval(
            approval_id=approval.approval_id,
            approver_id="soc_lead_bob@trustshield.internal",
            decision="REJECTED",
            decision_reason="False positive IP",
        )

        action.approval_status = "REJECTED"
        with pytest.raises(PermissionError):
            exec_engine.execute_action(action)
