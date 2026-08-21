import pytest
from app.services.threat_intelligence_fusion.intelligence_dissemination_engine import IntelligenceDisseminationEngine

def test_candidate_yara_rule_generation():
    engine = IntelligenceDisseminationEngine()
    yara = engine.generate_candidate_yara_rule(
        malware_family="Cobalt Strike Beacon",
        file_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert yara["format"] == "YARA"
    assert yara["lifecycle_state"] == "CANDIDATE"
    assert yara["requires_human_approval"] is True
    assert "Cobalt_Strike_Beacon" in yara["rule_content"]
