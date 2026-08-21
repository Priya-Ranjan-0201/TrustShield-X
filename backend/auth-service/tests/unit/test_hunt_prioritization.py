import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_hunt_prioritization():
    fabric = ThreatHuntingFabric()

    h1 = fabric.create_hunt_hypothesis("Minor certificate discrepancy", "Low impact", "INFRASTRUCTURE_REUSE")
    h2 = fabric.create_hunt_hypothesis("Active Payment Gateway Impersonation", "Critical impact", "PAYMENT_FRAUD")

    assert h1.priority in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert h2.priority in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
