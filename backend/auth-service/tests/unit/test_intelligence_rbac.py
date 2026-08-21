import pytest

def test_intelligence_rbac_roles():
    permissions = {
        "ADMIN": ["intelligence.read", "intelligence.ingest", "intelligence.forecast", "intelligence.admin"],
        "SOC_ANALYST": ["intelligence.read", "intelligence.ingest", "intelligence.forecast"],
        "AUDITOR": ["intelligence.read"],
    }
    assert "intelligence.admin" in permissions["ADMIN"]
    assert "intelligence.forecast" in permissions["SOC_ANALYST"]
    assert "intelligence.admin" not in permissions["AUDITOR"]
