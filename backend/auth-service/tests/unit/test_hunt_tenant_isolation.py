import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_hunt_tenant_isolation():
    fabric = ThreatHuntingFabric()

    fabric.create_hunt_hypothesis("Tenant A Hunt", "Desc A", "CAMPAIGN_EXPANSION", tenant_id="tenant_iso_a")
    fabric.create_hunt_hypothesis("Tenant B Hunt", "Desc B", "IMPERSONATION", tenant_id="tenant_iso_b")

    a_hunts = fabric.list_hypotheses("tenant_iso_a")
    b_hunts = fabric.list_hypotheses("tenant_iso_b")

    assert len(a_hunts) == 1
    assert a_hunts[0].title == "Tenant A Hunt"
    assert len(b_hunts) == 1
    assert b_hunts[0].title == "Tenant B Hunt"
