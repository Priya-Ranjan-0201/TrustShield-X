import pytest
import time
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_soc_performance_low_latency_processing():
    orch = SecurityOperationsOrchestrator()

    start = time.perf_counter()
    alert = orch.ingest_alert("tenant_perf", "WAF", "srv_checkout")
    clusters = orch.correlate_and_cluster("tenant_perf")
    p_dto = orch.priority_engine.compute_priority(alert)
    elapsed = time.perf_counter() - start

    assert elapsed < 0.1  # < 100ms
    assert p_dto.priority_score > 0
    assert len(clusters) >= 1
