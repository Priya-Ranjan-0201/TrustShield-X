import pytest
from app.services.security_engineering.improvement_generation_engine import ImprovementGenerationEngine

def test_improvement_evidence_integrity():
    engine = ImprovementGenerationEngine()
    imp = engine.get_improvement("imp_sigma_t1055_rule")
    assert len(imp.evidence) >= 2
    assert "ev_threat_intel_AP44" in imp.evidence
