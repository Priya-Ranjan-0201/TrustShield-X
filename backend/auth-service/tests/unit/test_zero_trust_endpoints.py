import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_zero_trust_endpoints_lifecycle():
    # 1. Register identity
    resp1 = client.post("/api/v1/zero-trust-exposure/identities/register", json={
        "identity_id": "EP-ID-01",
        "tenant_id": "tenant-test",
        "username": "test_user",
        "email": "test@test.com",
        "roles": ["ADMIN"],
        "permissions": ["all"],
        "mfa_enforced": True
    })
    assert resp1.status_code == 200
    assert resp1.json()["identity_id"] == "EP-ID-01"
    
    # 2. Discover EASM asset
    resp2 = client.post("/api/v1/zero-trust-exposure/easm/discover", json={
        "asset_id": "EP-EXT-01",
        "tenant_id": "tenant-test",
        "asset_type": "DOMAIN",
        "identifier": "api.test.com",
        "discovery_method": "PASSIVE_SCAN",
        "confidence": 1.0,
        "owner": "SecOps",
        "criticality": "HIGH"
    })
    assert resp2.status_code == 200
    assert resp2.json()["asset_id"] == "EP-EXT-01"
    
    # 3. List EASM assets
    resp3 = client.get("/api/v1/zero-trust-exposure/easm/assets/tenant-test")
    assert resp3.status_code == 200
    assert len(resp3.json()) >= 1
    
    # 4. Evaluate access
    resp4 = client.post("/api/v1/zero-trust-exposure/evaluate-access", json={
        "tenant_id": "tenant-test",
        "subject_id": "EP-ID-01",
        "device_id": "DEV-01",
        "session_id": "SESS-01",
        "resource_id": "RES-01",
        "resource_sensitivity": "PUBLIC",
        "action": "READ",
        "source_ip": "127.0.0.1"
    })
    assert resp4.status_code == 200
    assert "decision" in resp4.json()
