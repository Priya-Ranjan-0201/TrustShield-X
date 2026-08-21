import pytest
from app.services.security_engineering.security_root_cause_engine import SecurityRootCauseEngine

def test_root_cause_analysis_classification():
    engine = SecurityRootCauseEngine()
    rca = engine.analyze_root_cause("gap_123", category="ROOT_CAUSE", rationale="Missing sigma rule")
    assert rca.category == "ROOT_CAUSE"
    assert len(rca.supporting_evidence) >= 1
