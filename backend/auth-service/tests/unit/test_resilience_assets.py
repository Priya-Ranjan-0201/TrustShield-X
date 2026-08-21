import pytest
from app.services.resilience.resilience_asset_manager import ResilienceAssetManager
from app.schemas.cyber_resilience_models import ResilienceAssetDTO

def test_resilience_assets():
    mgr = ResilienceAssetManager()
    assets = mgr.list_assets()
    assert len(assets) >= 3
    ast = mgr.get_asset("ast_pg_primary")
    assert ast is not None
    assert ast.criticality == "CRITICAL"
    assert ast.recovery_strategy == "RESTORE_FROM_BACKUP"
