import pytest
from app.services.global_defense.crisis_communication_controller import CrisisCommunicationController

def test_communication_unsanitized_content_blocked():
    ctrl = CrisisCommunicationController()
    alert = ctrl.compose_and_validate_alert(
        sender_id="sender_1",
        recipients=["peer_1"],
        subject="Secret leak test",
        sanitized_content="Leaked password=SuperSecretPass123!",
    )
    assert alert["status"] == "SANITIZATION_REQUIRED"
    assert alert["sent"] is False
