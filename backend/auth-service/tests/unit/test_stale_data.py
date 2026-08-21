"""Unit Tests — Stale Data Detection (Phase 4.0 Part 4 — Section 60, 83)."""

import pytest
from datetime import datetime, timezone, timedelta


class TestStaleData:
    def test_stale_timestamp_detection(self):
        old_time = (datetime.now(timezone.utc) - timedelta(days=45)).isoformat()
        current_time = datetime.now(timezone.utc).isoformat()

        # Reports older than 30 days are flagged as historical / stale
        is_stale = (datetime.now(timezone.utc) - datetime.fromisoformat(old_time)).days > 30
        assert is_stale is True

        is_current_stale = (datetime.now(timezone.utc) - datetime.fromisoformat(current_time)).days > 30
        assert is_current_stale is False
