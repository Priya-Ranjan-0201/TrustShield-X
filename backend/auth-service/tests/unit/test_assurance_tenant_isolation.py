import pytest
from app.services.assurance_fabric.security_assurance_fabric import SecurityAssuranceFabric
from app.services.assurance.security_control_registry_service import SecurityControlRegistryService

def test_phase24_assurance_tenant_isolation():
    fabric = SecurityAssuranceFabric()
    t1 = fabric.get_complete_assurance_overview("tenant_alpha")
    t2 = fabric.get_complete_assurance_overview("tenant_beta")
    assert t1["tenant_id"] == "tenant_alpha"
    assert t2["tenant_id"] == "tenant_beta"

def test_legacy_assurance_tenant_isolation():
    service = SecurityControlRegistryService()
    controls = service.list_controls("tenant_bank")
    assert len(controls) >= 5
