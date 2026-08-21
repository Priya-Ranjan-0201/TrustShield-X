import pytest
from app.services.zero_trust_exposure.vulnerability_prioritization_engine import VulnerabilityPrioritizationEngine

def test_remediation_prioritization_cisa_kev():
    engine = VulnerabilityPrioritizationEngine()
    score = engine.prioritize_vulnerability(
        cve_id="CVE-2024-3094",
        tenant_id="t1",
        cvss_score=10.0,
        epss_score=0.95,
        is_in_cisa_kev=True,
        asset_criticality=5.0,
        is_reachable=True
    )
    assert score["priority_tier"] == "CRITICAL_EXPOSURE"
    assert score["calculated_risk_score"] >= 8.5
