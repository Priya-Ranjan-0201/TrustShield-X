import pytest
from app.services.mission_control.response_plan_engine import ResponsePlanEngine

def test_response_comparison():
    engine = ResponsePlanEngine()
    plan = engine.generate_response_plan("cmd_comp", [
        {"objective": "Option A", "reversibility": "FULLY_REVERSIBLE", "confidence": 0.85, "risk_reduction_score": 0.7, "blast_radius_reduction": 0.6, "service_disruption_score": 0.2, "execution_complexity": "LOW"},
        {"objective": "Option B", "reversibility": "PARTIALLY_REVERSIBLE", "confidence": 0.7, "risk_reduction_score": 0.9, "blast_radius_reduction": 0.9, "service_disruption_score": 0.7, "execution_complexity": "MEDIUM"},
    ])
    comparison = engine.compare_options(plan.plan_id)
    assert len(comparison) == 2
    assert comparison[0]["objective"] == "Option A"
    assert comparison[1]["risk_reduction"] == 0.9
