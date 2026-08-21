import pytest
from app.services.security_engineering.improvement_generation_engine import ImprovementGenerationEngine

def test_security_improvements_inventory():
    engine = ImprovementGenerationEngine()
    improvements = engine.list_improvements()
    assert len(improvements) >= 1
    imp = engine.get_improvement("imp_sigma_t1055_rule")
    assert imp is not None
    assert imp.category == "DETECTION"
    assert imp.reversibility == "FULLY_REVERSIBLE"
    assert imp.outcome_status == "IMPROVED"
