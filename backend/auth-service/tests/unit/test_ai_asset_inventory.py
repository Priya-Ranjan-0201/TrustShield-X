import pytest
from app.services.ai_governance.ai_asset_inventory_engine import AIAssetInventoryEngine

def test_ai_asset_inventory_listing():
    engine = AIAssetInventoryEngine()
    assets = engine.list_assets("default_tenant")
    assert len(assets) >= 2
    types = [a.type for a in assets]
    assert "CLASSIFIER" in types
    assert "LLM" in types
