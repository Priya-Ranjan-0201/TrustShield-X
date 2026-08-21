import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_alert_deduplication_into_clusters():
    orch = SecurityOperationsOrchestrator()
    a1 = orch.ingest_alert(tenant_id="tenant_a", source="WAF", asset="srv_web", indicator="198.51.100.42")
    a2 = orch.ingest_alert(tenant_id="tenant_a", source="SIEM", asset="srv_api", indicator="198.51.100.42")

    clusters = orch.correlate_and_cluster("tenant_a")
    assert len(clusters) >= 1
    assert a1.alert_id in clusters[0].alert_ids
    assert a2.alert_id in clusters[0].alert_ids
