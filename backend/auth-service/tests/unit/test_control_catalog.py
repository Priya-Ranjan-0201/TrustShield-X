import pytest
from app.services.enterprise_governance.control_catalog_engine import ControlCatalogEngine

def test_control_catalog_listing():
    engine = ControlCatalogEngine()
    controls = engine.list_controls("default_tenant")
    assert len(controls) >= 2
    assert controls[0].primary_owner is not None
    assert controls[0].backup_owner is not None
