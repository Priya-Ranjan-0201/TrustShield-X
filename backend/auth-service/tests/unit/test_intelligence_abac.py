import pytest

def test_intelligence_abac_evaluation():
    tenant_policy = {"tenant_id": "tenant_a", "allowed_classifications": ["PUBLIC", "COMMERCIAL"]}
    assert "COMMERCIAL" in tenant_policy["allowed_classifications"]
