import pytest
import time
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager


def test_knowledge_high_throughput_insertion():
    manager = KnowledgeObjectManager()

    start = time.perf_counter()
    for i in range(100):
        manager.create_object("INDICATOR", f"ioc_ip_192_0_2_{i}", tenant_id="tenant_perf")
    duration = time.perf_counter() - start

    assert duration < 0.5  # < 500ms for 100 objects
    assert len(manager.list_objects("tenant_perf")) == 100
