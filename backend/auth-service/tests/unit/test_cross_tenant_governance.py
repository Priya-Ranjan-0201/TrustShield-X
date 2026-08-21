import pytest
from app.services.enterprise_governance.control_catalog_engine import ControlCatalogEngine

def test_cross_tenant_control_isolation():
    engine = ControlCatalogEngine()
    controls = engine.list_controls("tenant_xyz")
    assert len(controls) == 0
