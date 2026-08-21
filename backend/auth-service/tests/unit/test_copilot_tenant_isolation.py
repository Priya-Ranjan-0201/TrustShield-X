import pytest
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_tenant_isolation():
    copilot = SecurityCopilot()

    session_a = copilot.create_session(tenant_id="tenant_alpha")
    session_b = copilot.create_session(tenant_id="tenant_beta")

    # Tenant alpha cannot retrieve tenant beta's session
    assert copilot.get_session(session_b.session_id, tenant_id="tenant_alpha") is None
    assert copilot.get_session(session_b.session_id, tenant_id="tenant_beta") is not None
