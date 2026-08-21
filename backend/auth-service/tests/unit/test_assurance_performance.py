import pytest
import time
from app.services.assurance_fabric.security_assurance_fabric import SecurityAssuranceFabric

def test_assurance_performance():
    fabric = SecurityAssuranceFabric()
    start = time.perf_counter()
    overview = fabric.get_complete_assurance_overview()
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1
    assert overview["overall_assurance_score"] > 0
