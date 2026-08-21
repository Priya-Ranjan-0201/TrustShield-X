import pytest
from app.services.threat_intelligence_fusion.vulnerability_intelligence_engine import VulnerabilityIntelligenceEngine

def test_cve_ingestion_and_cvss():
    engine = VulnerabilityIntelligenceEngine()
    vuln = engine.get_vulnerability("CVE-2026-3091")
    assert vuln is not None
    assert vuln.cvss_score == 9.8
    assert vuln.exploitation_status == "ACTIVELY_EXPLOITED"
