"""Unit tests for Behavior Rule REST API Endpoints (Phase 3.9 Part 1A.24)."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rules_endpoint_unauthorized():
    res = client.get("/api/v1/rules?scan_id=00000000-0000-0000-0000-000000000000")
    assert res.status_code in [401, 403]
