import pytest
from app.services.cyber_crisis_command.crisis_escalation_engine import CrisisEscalationEngine

def test_sla_status_checks():
    engine = CrisisEscalationEngine()
    # Containment SLA target is 60m for SEV_1
    healthy = engine.check_sla_status("C-SLA", "t1", "CONTAINMENT", elapsed_minutes=25, severity="SEV_1")
    assert healthy["status"] == "HEALTHY"
    
    breached = engine.check_sla_status("C-SLA", "t1", "CONTAINMENT", elapsed_minutes=75, severity="SEV_1")
    assert breached["status"] == "BREACHED"
