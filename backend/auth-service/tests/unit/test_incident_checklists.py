import pytest
from app.services.fusion.incident_command_engine import IncidentCommandEngine


def test_incident_checklist_completion_with_evidence():
    engine = IncidentCommandEngine()
    cmd = engine.create_incident_command("INC-02", "lead", "HIGH", tenant_id="tenant_chk")

    assert cmd.checklist[0].is_completed is False

    # Complete first checklist item with verified evidence
    updated = engine.complete_checklist_item(
        incident_id="INC-02",
        item_id="chk_1",
        evidence_id="ev_dns_01",
        verified_by="lead",
        tenant_id="tenant_chk",
    )
    assert updated.checklist[0].is_completed is True
    assert updated.checklist[0].evidence_id == "ev_dns_01"
    assert updated.next_action == updated.checklist[1].task_description
