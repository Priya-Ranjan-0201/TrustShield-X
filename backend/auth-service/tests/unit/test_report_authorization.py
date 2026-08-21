"""Unit tests for Report Endpoint Authorization (Phase 4.0 Part 1)."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_report_endpoint_unauthorized():
    res = client.get("/api/v1/reports/rep_unauthorized")
    assert res.status_code in [401, 403, 404]
