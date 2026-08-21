import pytest
from app.services.security_engineering.change_impact_analysis_engine import ChangeImpactAnalysisEngine

def test_impact_analysis():
    engine = ChangeImpactAnalysisEngine()
    impact = engine.analyze_impact(
        improvement_id="imp_123",
        affected_controls=["ctl_tenant_isolation"],
        affected_services=["app_auth_service"],
        affected_tenants=["default_tenant"],
    )
    assert impact.risk_classification == "LOW_RISK_REVERSIBLE"
    assert impact.requires_human_approval is False
