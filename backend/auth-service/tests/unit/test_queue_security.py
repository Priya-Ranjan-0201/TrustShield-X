import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_queue_security_tenant_isolation():
    orch = SecurityOperationsOrchestrator()
    a = orch.ingest_alert("tenant_queue_1", "QUEUE", "srv_1")
    assert a.tenant_id == "tenant_queue_1"
