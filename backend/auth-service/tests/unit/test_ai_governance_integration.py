import pytest
from app.services.ai_governance.ai_security_governance_engine import AISecurityGovernanceEngine

def test_ai_governance_cross_phase_integration():
    engine = AISecurityGovernanceEngine()
    summary = engine.get_governance_summary("default_tenant")
    assert summary["system_health"] == "HEALTHY"
