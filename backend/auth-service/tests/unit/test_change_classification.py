import pytest
from app.services.security_engineering.change_impact_analysis_engine import ChangeImpactAnalysisEngine

def test_change_classification():
    engine = ChangeImpactAnalysisEngine()
    low = engine.analyze_impact("imp_low", affected_tenants=["t1"])
    assert low.risk_classification == "LOW_RISK_REVERSIBLE"
