import pytest
from app.services.zero_trust_exposure.threat_exposure_orchestration_engine import ThreatExposureOrchestrationEngine

def test_soar_mobilization_dispatch():
    engine = ThreatExposureOrchestrationEngine()
    cycle = engine.initiate_ctem_cycle("CYC-01", "t1", "Production Perimeter", ["AWS", "Azure"])
    assert cycle["current_stage"] == "SCOPING"
    
    action = engine.mobilize_remediation("MOB-01", "CYC-01", "t1", "EXP-101", "MICROSEGMENT_POLICY")
    assert action["status"] == "DISPATCHED"
