import pytest
from app.services.assurance.security_control_registry_service import SecurityControlRegistryService


def test_test_freshness_tracking():
    service = SecurityControlRegistryService()

    # Core control is initialized with CURRENT freshness
    ctrl = service.get_control("ctrl_iso_01")
    assert ctrl is not None
    assert ctrl.freshness == "CURRENT"

    # Newly registered control without tests has NEVER_TESTED
    new_ctrl = service.register_control("Unchecked Service", "MONITORING", "Test")
    assert new_ctrl.freshness == "NEVER_TESTED"
