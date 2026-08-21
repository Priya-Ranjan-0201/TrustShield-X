import pytest
from app.services.resilience.business_validation_engine import BusinessValidationEngine

def test_frontend_recovery():
    engine = BusinessValidationEngine()
    res = engine.execute_synthetic_workflow("svc_checkout_api", "FRONTEND_RECONNECT_TEST")
    assert res.workflow_status == "VALIDATED"
