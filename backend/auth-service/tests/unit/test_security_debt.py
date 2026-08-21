import pytest
from app.services.assurance_fabric.security_debt_engine import SecurityDebtEngine

def test_security_debt():
    engine = SecurityDebtEngine()
    debt = engine.evaluate_debt(unverified_controls=1, coverage_gaps=2)
    assert debt.total_debt_score > 0
    assert len(debt.priority_recommendations) >= 2
