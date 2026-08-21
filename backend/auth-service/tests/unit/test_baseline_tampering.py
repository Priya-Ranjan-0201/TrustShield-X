import pytest
from app.services.assurance_fabric.security_baselines_engine import SecurityBaselinesEngine

def test_baseline_tampering():
    engine = SecurityBaselinesEngine()
    base = engine.get_baseline("sbase_v1_prod_locked")
    assert base is not None
    # Pydantic model is frozen
    with pytest.raises(Exception):
        base.version = "tampered_version"
