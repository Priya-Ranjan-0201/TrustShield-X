import pytest
from app.services.adaptive_defense.defense_change_manager import DefenseChangeManager


def test_change_collision_prevention():
    manager = DefenseChangeManager()
    manager.schedule_change("tenant_1", "ISOLATE", "ep-001", "Threat containment")

    # Concurrent attempt on same target must raise collision error
    with pytest.raises(ValueError) as exc:
        manager.schedule_change("tenant_1", "RECONFIGURE", "ep-001", "Config change")

    assert "Change collision detected" in str(exc.value)
