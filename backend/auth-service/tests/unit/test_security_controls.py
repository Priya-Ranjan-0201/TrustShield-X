import pytest
from app.services.assurance_fabric.control_inventory_manager import ControlInventoryManager

def test_security_controls_inventory():
    mgr = ControlInventoryManager()
    controls = mgr.list_controls()
    assert len(controls) >= 3
    ctl = mgr.get_control("ctl_tenant_isolation")
    assert ctl is not None
    assert ctl.criticality == "CRITICAL"
    assert ctl.category == "TENANT_ISOLATION"
    assert ctl.validation_status == "PASS"
