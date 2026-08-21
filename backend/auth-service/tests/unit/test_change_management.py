import pytest
from app.services.adaptive_defense.defense_change_manager import DefenseChangeManager


def test_defense_change_lifecycle():
    manager = DefenseChangeManager()
    change = manager.schedule_change(
        tenant_id="tenant_chg",
        action_type="NETWORK_CONTROL",
        target="198.51.100.44",
        reason="Block C2 traffic",
    )

    assert change.change_id.startswith("chg_")
    assert change.execution_status == "SCHEDULED"

    updated = manager.record_execution_result(change.change_id, "SUCCEEDED", {"rules_updated": 1})
    assert updated.execution_status == "SUCCEEDED"
    assert updated.executed_at is not None
