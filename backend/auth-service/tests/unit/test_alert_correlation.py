import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_alert_correlation_shared_indicators():
    orch = SecurityOperationsOrchestrator()
    orch.ingest_alert(tenant_id="t1", source="WAF", asset="srv_1", indicator="c2.shadowhydra.net")
    orch.ingest_alert(tenant_id="t1", source="EDR", asset="srv_2", indicator="c2.shadowhydra.net")

    clusters = orch.correlate_and_cluster("t1")
    assert len(clusters) == 1
    assert len(clusters[0].alert_ids) == 2
