import pytest
from app.services.assurance.security_control_registry_service import SecurityControlRegistryService


def test_ai_model_assurance():
    service = SecurityControlRegistryService()
    ai_ctrl = service.get_control("ctrl_ai_01")

    assert ai_ctrl is not None
    assert ai_ctrl.category == "AI_SECURITY"
    assert ai_ctrl.verification_state == "VERIFIED"
