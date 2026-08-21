import pytest
from app.services.exposure.asset_baseline_engine import AssetBaselineEngine


def test_asset_baseline_establishment_and_versioning():
    engine = AssetBaselineEngine()
    b1 = engine.establish_baseline(
        asset_id="ast_101",
        dns_records={"A": ["198.51.100.22"]},
        exposed_ports=[80, 443],
        trust_score=90.0,
        risk_score=10.0,
        tenant_id="tenant_base",
    )
    assert b1.version == 1
    assert b1.exposed_ports == [80, 443]

    # Increment baseline with new port
    b2 = engine.establish_baseline(
        asset_id="ast_101",
        dns_records={"A": ["198.51.100.22"]},
        exposed_ports=[80, 443, 8443],
        trust_score=90.0,
        risk_score=10.0,
        tenant_id="tenant_base",
    )
    assert b2.version == 2
    assert 8443 in b2.exposed_ports

    history = engine.get_baseline_history("ast_101", "tenant_base")
    assert len(history) == 2
