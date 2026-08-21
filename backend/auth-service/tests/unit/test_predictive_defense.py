import pytest
from app.services.soc.incident_blast_radius_engine import IncidentBlastRadiusEngine


def test_predictive_defense_potential_asset_forecasting():
    engine = IncidentBlastRadiusEngine()
    deps = {"srv_payment": ["db_vault", "srv_ledger"]}
    br = engine.evaluate_blast_radius("inc_pred_01", ["srv_payment"], deps)

    assert "db_vault" in br.potential_impact_assets
    assert len(br.potential_impact_assets) == 2
