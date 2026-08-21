import pytest
from app.services.assurance.security_control_registry_service import SecurityControlRegistryService


def test_security_control_registry_lifecycle():
    service = SecurityControlRegistryService()

    # Register new control
    ctrl = service.register_control(
        name="Custom Web Application Firewall Rule",
        category="PREVENTIVE",
        description="Filters SQL injection and XSS attempts on public API gateway",
        criticality="HIGH",
        tenant_id="tenant_assure_01",
    )

    assert ctrl.control_id.startswith("ctrl_")
    assert ctrl.status == "REGISTERED"
    assert ctrl.verification_state == "DOCUMENTED"

    # Update verification state after validation
    updated = service.update_verification_state(ctrl.control_id, "VERIFIED", "ACTIVE")
    assert updated.verification_state == "VERIFIED"
    assert updated.status == "ACTIVE"
    assert updated.version == 2
