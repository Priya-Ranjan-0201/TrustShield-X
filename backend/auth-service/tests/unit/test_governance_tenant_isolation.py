import pytest
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_governance_tenant_isolation():
    collector = GovernanceEvidenceCollector()

    # Record tenant A and B evidence
    collector.record_evidence("ctrl_iso_01", "SRC_A", {"tenant": "A"}, tenant_id="tenant_gov_a")
    collector.record_evidence("ctrl_iso_01", "SRC_B", {"tenant": "B"}, tenant_id="tenant_gov_b")

    ev_a = collector.list_evidence("tenant_gov_a")
    tenant_ids_a = [e.tenant_id for e in ev_a]
    assert "tenant_gov_a" in tenant_ids_a
    assert "tenant_gov_b" not in tenant_ids_a
