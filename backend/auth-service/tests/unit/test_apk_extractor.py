"""Unit tests for APK Extraction Engine & Security Safeguards (Phase 3.7 Part 1A.4)."""

import os
import zipfile
import tempfile
import pytest
from app.services.apk_extractor import APKExtractor


@pytest.fixture
def sample_apk(tmp_path):
    apk_path = os.path.join(tmp_path, "sample.apk")
    with zipfile.ZipFile(apk_path, "w") as zf:
        zf.writestr("AndroidManifest.xml", b"<manifest package='com.test'></manifest>")
        zf.writestr("classes.dex", b"dex\n035\x00" + b"\x00" * 50)
        zf.writestr("res/drawable/icon.png", b"\x89PNG\r\n\x1a\n" + b"\x00" * 20)
    return apk_path


def test_apk_extractor_success(sample_apk, tmp_path):
    extractor = APKExtractor()
    out_dir = os.path.join(tmp_path, "workspace_out")
    res = extractor.extract_apk(sample_apk, out_dir)

    assert len(res.errors) == 0
    assert res.extracted_files_count == 3
    assert os.path.exists(os.path.join(out_dir, "AndroidManifest.xml"))
    assert os.path.exists(os.path.join(out_dir, "classes.dex"))


def test_apk_extractor_path_traversal_rejection(tmp_path):
    bad_apk = os.path.join(tmp_path, "bad.apk")
    with zipfile.ZipFile(bad_apk, "w") as zf:
        zf.writestr("../evil.sh", b"echo pwned")

    extractor = APKExtractor()
    out_dir = os.path.join(tmp_path, "workspace_bad")
    res = extractor.extract_apk(bad_apk, out_dir)

    assert len(res.errors) > 0
    assert "PATH_TRAVERSAL_DETECTED" in res.errors[0] or "Path traversal" in res.errors[0]
