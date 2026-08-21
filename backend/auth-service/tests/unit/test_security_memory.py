import pytest
from app.services.knowledge_fabric.security_memory_engine import SecurityMemoryEngine


def test_security_memory_tenant_storage():
    engine = SecurityMemoryEngine()

    engine.store_memory(
        tenant_id="tenant_x",
        category="DEFENSE_OUTCOME",
        title="Automated Rate Limiting on Checkout Ingress",
        details={"result": "Mitigated DDoS attack in 30 seconds"},
    )

    mem_x = engine.list_memories("tenant_x")
    mem_y = engine.list_memories("tenant_y")

    assert len(mem_x) == 1
    assert len(mem_y) == 0
