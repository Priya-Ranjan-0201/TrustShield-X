import pytest
from app.services.autonomous_defense.security_memory_engine import SecurityMemoryEngine

def test_tenant_generalization_isolation():
    engine = SecurityMemoryEngine()
    t_a_lessons = engine.get_applicable_lessons("default_tenant")
    assert len(t_a_lessons) >= 1
    
    t_b_lessons = engine.get_applicable_lessons("isolated_tenant_b")
    assert len(t_b_lessons) == 0
