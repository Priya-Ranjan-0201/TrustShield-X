import pytest
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine

def test_risky_public_port_exposure():
    engine = ExternalAttackSurfaceEngine()
    # Exposing DB port 5432 and RDP 3389 publicly
    asset = engine.register_public_asset(
        asset_id="EXT-RISKY-PORT",
        tenant_id="t1",
        domain_or_ip="203.0.113.99",
        open_ports=[80, 443, 5432, 3389]
    )
    assert asset["risk_score"] >= 8.0
    assert len(asset["vulnerabilities"]) > 0
