import pytest
from app.services.enterprise_governance.control_catalog_engine import ControlCatalogEngine

def test_control_lifecycle_states():
    engine = ControlCatalogEngine()
    ctrl = engine.get_control("ctrl_iam_mfa_enforcement")
    assert ctrl is not None
    assert ctrl.status in ("DRAFT", "ACTIVE", "TESTING", "VERIFIED", "FAILED", "DEPRECATED", "RETIRED")
