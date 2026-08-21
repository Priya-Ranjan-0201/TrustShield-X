import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_e2e_query_flow():
    copilot = TruthShieldSecurityCopilot()
    q = copilot.query_copilot("Explain situation on API Gateway", "t1", "analyst1", mode="SOC_ANALYST")
    assert q["status"] == "SUCCESS"
    
    hunt = copilot.generate_hunt_hypothesis("Encoded command", "t1")
    assert hunt["status"] == "AI_GENERATED"
    
    rule = copilot.generate_detection_rule("Ransomware persistence", "t1")
    assert rule["syntax_valid"] is True
