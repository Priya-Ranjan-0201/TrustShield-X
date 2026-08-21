"""Unit Tests — Investigation Privacy & Redaction (Phase 4.0 Part 4 — Section 79, 83)."""

import pytest
from app.services.renderers.json_report_renderer import _redact_dict


class TestInvestigationPrivacy:
    def test_sensitive_credentials_redacted_in_investigation(self):
        data = {
            "finding_id": "F_01",
            "password": "supersecretpass",
            "access_token": "eyJhbGciOiJIUzI1NiJ9",
            "observation": "Found sensitive data",
        }
        redacted = _redact_dict(data)
        assert redacted["password"] == "[REDACTED_SECRET]"
        assert redacted["access_token"] == "[REDACTED_SECRET]"
        assert redacted["finding_id"] == "F_01"
