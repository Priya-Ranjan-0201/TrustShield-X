import pytest
from app.services.digital_twin_lab.twin_synchronization_engine import TwinSynchronizationEngine

def test_twin_synchronization_telemetry_pipeline():
    engine = TwinSynchronizationEngine()
    res = engine.synchronize_twin(telemetry_source="KAFKA_TELEMETRY_MIRROR")
    assert res["freshness"] == "FRESH"
    assert res["synced_entities"] == 150
