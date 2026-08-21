import pytest
from app.services.security_engineering.change_impact_analysis_engine import ChangeImpactAnalysisEngine

def test_improvement_abac():
    engine = ChangeImpactAnalysisEngine()
    impact = engine.analyze_impact("imp_1", affected_tenants=["tenant_1"])
    assert impact.blast_radius_score <= 0.30
