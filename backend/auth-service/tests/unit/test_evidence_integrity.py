import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_evidence_integrity_detection():
    engine = CyberCrisisCommandEngine()
    engine.add_evidence_node("NODE-INT", "t1", "C-01", "VULN", {"cve": "CVE-2024-3094"})
    
    # Valid integrity check
    valid = engine.verify_evidence_integrity("NODE-INT", {"cve": "CVE-2024-3094"})
    assert valid["integrity_passed"] is True
    
    # Tampered payload fails
    tampered = engine.verify_evidence_integrity("NODE-INT", {"cve": "CVE-2024-9999"})
    assert tampered["integrity_passed"] is False
    assert tampered["status"] == "EVIDENCE_INTEGRITY_FAILURE"
