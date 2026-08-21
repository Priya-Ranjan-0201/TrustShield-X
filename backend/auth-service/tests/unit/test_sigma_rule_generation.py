import pytest
from app.services.threat_intelligence_fusion.intelligence_dissemination_engine import IntelligenceDisseminationEngine

def test_candidate_sigma_rule_generation():
    engine = IntelligenceDisseminationEngine()
    sigma = engine.generate_candidate_sigma_rule(
        indicator_value="malicious-c2.darkstorm-threat.com",
        technique_id="T1071.001",
        campaign_name="Operation DarkStorm"
    )
    assert sigma["format"] == "SIGMA_YAML"
    assert sigma["lifecycle_state"] == "CANDIDATE"
    assert sigma["requires_human_approval"] is True
    assert "malicious-c2.darkstorm-threat.com" in sigma["rule_content"]
