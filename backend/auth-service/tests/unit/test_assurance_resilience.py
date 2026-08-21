import pytest
from app.services.assurance_fabric.security_assurance_fabric import SecurityAssuranceFabric

def test_assurance_resilience():
    fabric = SecurityAssuranceFabric()
    for _ in range(50):
        overview = fabric.get_complete_assurance_overview()
        assert overview["security_controls_count"] >= 3
