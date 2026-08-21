import pytest
from app.services.knowledge_fabric.historical_analog_engine import HistoricalAnalogEngine


def test_recovery_reasoning_bottlenecks():
    engine = HistoricalAnalogEngine()
    lessons = engine.list_lessons_learned()

    assert len(lessons) >= 1
    assert any("secret rotation" in b.lower() for b in lessons[0].recovery_bottlenecks)
