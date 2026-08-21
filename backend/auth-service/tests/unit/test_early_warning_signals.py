import pytest
from app.services.threat_intelligence_fusion.threat_early_warning_engine import ThreatEarlyWarningEngine

def test_early_warning_signals_generation():
    engine = ThreatEarlyWarningEngine()
    warn = engine.generate_early_warning(
        reason="DDoS attack command surge observed across multiple botnet C2 nodes",
        evidence=["ev_honeypot_ddos_surge"],
        urgency="CRITICAL",
        affected_assets=["ast_payment_gw_01"],
        recommended_actions=["Engage Cloud Scrubbing Service"],
        confidence=0.96
    )
    assert warn.urgency == "CRITICAL"
    assert len(warn.recommended_actions) == 1
