"""Unit tests for Risk Aggregation REST API Authentication (Phase 3.9 Part 1B)."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_risk_endpoint_unauthorized():
    res = client.get("/api/v1/risk/assessment?scan_id=00000000-0000-0000-0000-000000000000")
    assert res.status_code in [401, 403]
