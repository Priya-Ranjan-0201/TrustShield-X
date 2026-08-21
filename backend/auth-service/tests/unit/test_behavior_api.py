"""Unit tests for Behavioral Correlation REST API Endpoints (Phase 3.9 Part 1A.22)."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_behavior_findings_endpoint_unauthorized():
    res = client.get("/api/v1/behavior/findings?scan_id=00000000-0000-0000-0000-000000000000")
    assert res.status_code in [401, 403]
