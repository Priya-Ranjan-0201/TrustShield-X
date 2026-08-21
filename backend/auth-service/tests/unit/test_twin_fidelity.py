import pytest
from app.services.cyber_digital_twin.cyber_digital_twin_engine import CyberDigitalTwinEngine

def test_twin_fidelity_dimensions():
    engine = CyberDigitalTwinEngine()
    engine.create_environment("ENV-FID", "t1", initial_state={"vulnerabilities": ["CVE-2024-3094"], "controls": ["MFA", "EDR"]})
    fid = engine.calculate_fidelity("ENV-FID", "t1")
    assert fid["overall_fidelity"] >= 0.90
    assert fid["asset_fidelity"] == 0.98
