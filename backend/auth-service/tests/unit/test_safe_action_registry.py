import pytest
from app.services.adaptive_defense.safe_defense_action_registry import SafeDefenseActionRegistry, ProtectedTargetViolationError


def test_safe_action_registry_defaults():
    registry = SafeDefenseActionRegistry()
    actions = registry.list_actions()
    assert len(actions) >= 4

    block_act = registry.get_action_definition("BLOCK_EXTERNAL_IP")
    assert block_act is not None
    assert block_act.requires_approval is False


def test_protected_targets_blocked():
    registry = SafeDefenseActionRegistry()

    assert registry.validate_target_safety("external-ip-198.51.100.4") is True

    with pytest.raises(ProtectedTargetViolationError):
        registry.validate_target_safety("localhost")

    with pytest.raises(ProtectedTargetViolationError):
        registry.validate_target_safety("127.0.0.1")

    with pytest.raises(ProtectedTargetViolationError):
        registry.validate_target_safety("production-db-primary")
