import pytest
from app.services.security_engineering.security_gap_engine import SecurityGapEngine

def test_assurance_improvement():
    engine = SecurityGapEngine()
    g = engine.create_gap(
        title="Repeated Tenant Isolation Assertion Failure",
        description="Staging cluster failed automated cross-tenant boundary validation",
        source="FAILED_VALIDATION",
    )
    assert g.source == "FAILED_VALIDATION"
