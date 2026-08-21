import pytest
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService


def test_simulation_tenant_isolation():
    service = DigitalSecurityTwinService()

    twin_a = service.create_twin_from_snapshot("snap_a", [], tenant_id="tenant_sim_a")
    twin_b = service.create_twin_from_snapshot("snap_b", [], tenant_id="tenant_sim_b")

    # Tenant B cannot access Twin A
    assert service.get_twin(twin_a.twin_id, tenant_id="tenant_sim_b") is None
    # Tenant A can access Twin A
    assert service.get_twin(twin_a.twin_id, tenant_id="tenant_sim_a") is not None
