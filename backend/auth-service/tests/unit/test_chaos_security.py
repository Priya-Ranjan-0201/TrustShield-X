import pytest
from app.services.cyber_digital_twin.digital_twin_validation_governance_engine import DigitalTwinValidationGovernanceEngine

def test_chaos_security_simulation():
    engine = DigitalTwinValidationGovernanceEngine()
    chaos = engine.execute_chaos_security_test("CHAOS-01", "t1", "FIREWALL", "TOTAL_OUTAGE")
    assert chaos["is_simulation"] is True
    assert chaos["observed_failover_status"] == "FAIL_SAFE_DEFAULT_DENY_ENFORCED"
    assert chaos["unauthorized_access_permitted"] is False
