import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_multi_tenant_soc_partitioning():
    orch = SecurityOperationsOrchestrator()
    orch.ingest_alert("tenant_x", "WAF", "srv_x", indicator="10.0.0.1")
    orch.ingest_alert("tenant_y", "WAF", "srv_y", indicator="10.0.0.1")

    clsts_x = orch.correlate_and_cluster("tenant_x")
    clsts_y = orch.correlate_and_cluster("tenant_y")

    assert len(clsts_x) == 1
    assert len(clsts_y) == 1
    assert clsts_x[0].tenant_id == "tenant_x"
    assert clsts_y[0].tenant_id == "tenant_y"
