import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_incident_creation_from_alert_cluster():
    orch = SecurityOperationsOrchestrator()
    a1 = orch.ingest_alert("tenant_inc", "EDR", "srv_checkout", "CRITICAL")
    clusters = orch.correlate_and_cluster("tenant_inc")

    assert len(clusters) >= 1
    assert a1.alert_id in clusters[0].alert_ids
