"""Unit tests for Evidence Consolidation REST API Authentication (Phase 3.9 Part 1A.25)."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_evidence_endpoint_unauthorized():
    res = client.get("/api/v1/evidence/findings?scan_id=00000000-0000-0000-0000-000000000000")
    assert res.status_code in [401, 403]
