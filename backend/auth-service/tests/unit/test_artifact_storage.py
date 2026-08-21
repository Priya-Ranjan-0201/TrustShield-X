"""Unit Tests — Artifact Storage Provider (Phase 4.0 Part 3 — Section 48-49)."""

import os
import shutil
import pytest
from app.services.storage.artifact_storage_provider import LocalStorageProvider, sanitize_filename


class TestArtifactStorage:
    """Sections 48-49: Local Storage Provider CRUD and path safety."""

    def setup_method(self):
        self.test_dir = "tests/test_storage_artifacts"
        self.provider = LocalStorageProvider(base_dir=self.test_dir)

    def teardown_method(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_put_get_exists_delete(self):
        key = "test_artifact.pdf"
        data = b"%PDF-1.4 test payload"
        stored_path = self.provider.put(key, data, content_type="application/pdf")
        assert os.path.exists(stored_path)
        assert self.provider.exists(key) is True

        retrieved = self.provider.get(key)
        assert retrieved == data

        meta = self.provider.metadata(key)
        assert meta["size_bytes"] == len(data)

        deleted = self.provider.delete(key)
        assert deleted is True
        assert self.provider.exists(key) is False

    def test_sanitize_filename(self):
        assert sanitize_filename("../../../etc/passwd") == "passwd"
        assert sanitize_filename("test\\dir\\report.pdf") == "report.pdf"
