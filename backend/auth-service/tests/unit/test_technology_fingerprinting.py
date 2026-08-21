import pytest
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine

def test_technology_fingerprinting():
    engine = ExternalAttackSurfaceEngine()
    fp = engine.fingerprint_technology("EXT-ASSET-01", "t1", "FastAPI", "Uvicorn", version="0.110.0", confidence=0.98)
    assert fp["web_framework"] == "FastAPI"
    assert fp["confidence"] == 0.98
