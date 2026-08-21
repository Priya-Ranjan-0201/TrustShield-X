import pytest
from app.services.resilience.business_validation_engine import BusinessValidationEngine

def test_failed_recovery():
    engine = BusinessValidationEngine()
    res = engine.execute_synthetic_workflow("svc_checkout_api", simulate_failure=True)
    assert res.workflow_status == "FAILED"
