import pytest
from app.services.global_defense.crisis_communication_controller import CrisisCommunicationController

def test_crisis_management_alert_dispatch():
    ctrl = CrisisCommunicationController()
    alert = ctrl.compose_and_validate_alert(
        sender_id="ciso_alpha",
        recipients=["tenant_finance_alpha", "tenant_cloud_beta"],
        subject="DarkStorm Synchronized Rate-Limiting Directive",
        sanitized_content="All peers deploy rate limiting on /api/v1/auth.",
        classification="CONFIDENTIAL",
    )
    assert alert["status"] == "DISPATCHED"
    assert alert["sent"] is True
