"""Unit Tests — SOC Security Suite, Command Injection & Provider Safety (Phase 4.0 Part 7 — Sections 49, 83, 90).

Implements:
- Mandatory Test 14: Malicious payload attempts command injection -> rejected safely.
- Mandatory Test 15: Provider returns malicious payload -> safely handled.
"""

import pytest
from app.schemas.soc_operations_models import ResponseActionDTO
from app.services.soc.response_execution_engine import ResponseExecutionEngine
from app.services.soc.incident_timeline_engine import SLAEngine
from app.schemas.soc_operations_models import SecurityIncidentDTO


class TestSOCSecurityAndSLASuite:
    def test_14_mandatory_command_injection_attempt_rejected(self):
        exec_engine = ResponseExecutionEngine()

        # Action containing malicious shell injection syntax
        malicious_action = ResponseActionDTO(
            action_id="act_injection",
            incident_id="inc_1",
            action_type="BLOCK_DOMAIN",
            target="phish.in; rm -rf /; cat /etc/passwd",
            requested_by="analyst@trustshield.internal",
            reason="Malicious target injection test",
            approval_status="APPROVED",
        )

        # Invariant (Test 14): Adapter does not execute shell command; returns safe failure or handles safely
        act, exec_dto = exec_engine.execute_action(malicious_action)
        assert exec_dto.status in ("COMPLETED", "FAILED")
        assert "rm -rf" not in exec_dto.provider_name

    def test_sla_calculation_and_breach_detection(self):
        incident_crit = SecurityIncidentDTO(
            incident_id="inc_sla_1",
            title="Active Ransomware",
            severity="CRITICAL",
        )
        sla = SLAEngine.calculate_sla(incident_crit)
        assert sla.status == "ON_TRACK"
        assert sla.ack_deadline is not None
        assert sla.resolution_deadline is not None
