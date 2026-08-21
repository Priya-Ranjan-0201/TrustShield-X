import pytest
from app.services.knowledge_fabric.historical_analog_engine import HistoricalAnalogEngine


def test_historical_analogs_matching():
    engine = HistoricalAnalogEngine()
    analogs = engine.find_analogs(["T1566.002"])

    assert len(analogs) >= 1
    assert analogs[0].past_incident_id == "inc_2025_q4_0012"
    assert analogs[0].similarity_score > 0.85
