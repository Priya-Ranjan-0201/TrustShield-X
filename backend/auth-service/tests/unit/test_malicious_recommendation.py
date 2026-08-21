import pytest
from app.services.security_engineering.improvement_generation_engine import ImprovementGenerationEngine

def test_malicious_recommendation():
    engine = ImprovementGenerationEngine()
    # Attempting to propose disabling authentication must be rejected immediately
    with pytest.raises(ValueError, match="Malicious Recommendation Rejected"):
        engine.generate_improvement(
            category="ACCESS_CONTROL",
            title="Disable Authentication on Internal API",
            description="To improve speed, disable auth check on gateway",
            problem="Latency",
            proposed_change="disable authentication",
            expected_benefit="Speed",
            expected_risk="None",
        )
