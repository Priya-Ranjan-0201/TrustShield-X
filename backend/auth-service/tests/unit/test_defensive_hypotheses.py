import pytest
from app.services.global_intelligence.defensive_hypothesis_engine import DefensiveHypothesisEngine

def test_defensive_hypothesis_generation():
    engine = DefensiveHypothesisEngine()
    hyp = engine.generate_hypothesis(
        threat_id="cmp_darkstorm_2026",
        statement="If rate-limiting is deployed, DarkStorm blast radius is reduced by 80%.",
        testable_criteria="Simulated containment latency < 25s",
    )
    assert hyp.digital_twin_scenario_id == "scen_phishing_lateral_movement"
    assert "Digital Twin" in hyp.recommended_validation
