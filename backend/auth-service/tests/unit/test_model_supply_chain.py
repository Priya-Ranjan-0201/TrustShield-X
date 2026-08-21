import pytest
from app.services.ai_governance.model_supply_chain_engine import ModelSupplyChainEngine

def test_model_supply_chain_scan():
    engine = ModelSupplyChainEngine()
    res = engine.scan_dependencies("mdl_c2_neural_classifier", ["torch==2.6.0", "transformers==4.49.0"])
    assert res["is_secure"] is True
    assert res["findings_count"] == 0
