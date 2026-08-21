import pytest
from app.services.autonomous_defense.security_memory_engine import SecurityMemoryEngine

def test_security_memory_lessons_retrieval():
    engine = SecurityMemoryEngine()
    lessons = engine.get_applicable_lessons("default_tenant")
    assert len(lessons) >= 1
    assert lessons[0].status == "LEARNED"
