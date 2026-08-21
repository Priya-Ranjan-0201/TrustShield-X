import pytest
from app.services.enterprise_governance.exception_management_engine import ExceptionManagementEngine

def test_exception_management_expiration():
    engine = ExceptionManagementEngine()
    
    # Active within timeframe
    res_active = engine.inspect_exception_status("exc_legacy_mainframe_probe", current_time_iso="2026-08-20T00:00:00Z")
    assert res_active["is_active"] is True
    assert res_active["status"] == "ACTIVE"
    
    # Expired past timeframe
    res_exp = engine.inspect_exception_status("exc_legacy_mainframe_probe", current_time_iso="2026-09-10T00:00:00Z")
    assert res_exp["is_active"] is False
    assert res_exp["status"] == "EXCEPTION_EXPIRED"
