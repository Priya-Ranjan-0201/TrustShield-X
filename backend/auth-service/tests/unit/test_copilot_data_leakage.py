import pytest
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_cross_tenant_data_leakage_block():
    copilot = SecurityCopilot()

    session_x = copilot.create_session(tenant_id="tenant_x")
    session_y = copilot.create_session(tenant_id="tenant_y")

    # Tenant X cannot fetch session Y
    assert copilot.get_session(session_y.session_id, tenant_id="tenant_x") is None
