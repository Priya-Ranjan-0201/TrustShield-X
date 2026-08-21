import pytest
from app.services.autonomous_defense.security_memory_engine import SecurityMemoryEngine

def test_lesson_tenant_boundaries():
    engine = SecurityMemoryEngine()
    # Tenant B should not receive Tenant A's tenant-specific lessons
    tenant_b_lessons = engine.get_applicable_lessons("tenant_b", allow_cross_tenant=False)
    assert len(tenant_b_lessons) == 0
