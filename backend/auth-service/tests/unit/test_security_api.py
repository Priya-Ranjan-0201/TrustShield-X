import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_security_overview_and_posture_endpoints():
    res = client.get("/api/v1/security/overview?tenant_id=test_api_tenant")
    assert res.status_code == 200
    data = res.json()
    assert "posture" in data
    assert "situation" in data
    assert "kpis" in data
    assert "health" in data


def test_security_events_and_narrative_endpoints():
    res_nar = client.get("/api/v1/security/narrative/corp-portal.com")
    assert res_nar.status_code == 200
    data_nar = res_nar.json()
    assert "what_happened" in data_nar
    assert "what_is_verified" in data_nar
    assert "what_remains_unknown" in data_nar
