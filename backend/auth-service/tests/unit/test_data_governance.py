import pytest
from app.services.enterprise_governance.control_catalog_engine import ControlCatalogEngine

def test_data_governance_encryption_control():
    engine = ControlCatalogEngine()
    ctrl = engine.get_control("ctrl_data_encryption_at_rest")
    assert ctrl is not None
    assert ctrl.domain == "DATA_PROTECTION"
