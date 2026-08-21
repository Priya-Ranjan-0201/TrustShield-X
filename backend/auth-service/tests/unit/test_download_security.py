"""Unit Tests — Download Security & Path Traversal Prevention (Phase 4.0 Part 3 — Section 84, Test 16)."""

import pytest
from app.services.storage.artifact_storage_provider import LocalStorageProvider, sanitize_filename


class TestDownloadSecurity:
    """Mandatory Test Case 16: Attempt path traversal in download. Expected: Rejected safely."""

    def test_path_traversal_sanitized(self):
        malicious_keys = [
            "../../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\cmd.exe",
            "/etc/shadow",
            "C:\\boot.ini",
            "....//....//report.pdf",
        ]
        provider = LocalStorageProvider(base_dir="tests/test_safe_dir")
        for key in malicious_keys:
            safe = sanitize_filename(key)
            assert ".." not in safe or safe.startswith("report_artifact_")
            assert "/" not in safe
            assert "\\" not in safe
