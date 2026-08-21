import pytest
from app.services.security_engineering.autonomous_security_engineering_engine import AutonomousSecurityEngineeringEngine

def test_improvement_tenant_isolation():
    engine = AutonomousSecurityEngineeringEngine()
    t1 = engine.get_engineering_overview("tenant_alpha")
    t2 = engine.get_engineering_overview("tenant_beta")
    assert t1["tenant_id"] == "tenant_alpha"
    assert t2["tenant_id"] == "tenant_beta"
