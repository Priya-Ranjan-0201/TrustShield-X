import pytest
from app.services.assurance_fabric.security_baselines_engine import SecurityBaselinesEngine

def test_security_baselines():
    engine = SecurityBaselinesEngine()
    base = engine.get_baseline("sbase_v1_prod_locked")
    assert base is not None
    assert base.immutable_hash is not None
    assert base.control_states["ctl_tenant_isolation"] == "PASS"
