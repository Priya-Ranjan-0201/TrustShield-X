import pytest
from app.services.assurance.security_control_registry_service import SecurityControlRegistryService


def test_control_health_transitions():
    service = SecurityControlRegistryService()

    # Degraded state transition
    service.update_verification_state("ctrl_waf_01", "DEGRADED", "DEGRADED")
    ctrl = service.get_control("ctrl_waf_01")
    assert ctrl is not None
    assert ctrl.verification_state == "DEGRADED"

    # Recovered state transition
    service.update_verification_state("ctrl_waf_01", "VERIFIED", "ACTIVE")
    ctrl_rec = service.get_control("ctrl_waf_01")
    assert ctrl_rec is not None
    assert ctrl_rec.verification_state == "VERIFIED"
