import pytest
from app.services.global_defense.crisis_communication_controller import CrisisCommunicationController

def test_communication_control_empty_recipients_rejected():
    ctrl = CrisisCommunicationController()
    with pytest.raises(ValueError, match="Recipients list cannot be empty"):
        ctrl.compose_and_validate_alert("sender_1", [], "Subject", "Content")
