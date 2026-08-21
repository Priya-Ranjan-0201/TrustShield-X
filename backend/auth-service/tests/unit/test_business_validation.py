import pytest
from app.services.resilience.business_validation_engine import BusinessValidationEngine

def test_business_validation():
    engine = BusinessValidationEngine()
    res = engine.execute_synthetic_workflow("svc_checkout_api", "SYNTHETIC_TRANSACTION")
    assert res.workflow_status == "VALIDATED"
    assert res.latency_ms > 0
