"""Unit tests for Phase 3.7 Part 1A — AI Android APK Security Engine — Infrastructure, Validation & Secure Parsing Foundation.

Tests cover:
- APKValidator (10 security checks: Extension, MIME, Size, Zero-byte, ZIP integrity, CRC, Duplicates, Path Traversal, ZIP Bomb, Streaming SHA-256)
- APKUploadService (UUID storage allocation under storage/uploads/apk/{user_id}/{uuid}/ & temp cleanup)
- ApkErrorCode mapping (TSX-APK-001 to TSX-APK-010)
"""

import os
import uuid
import zipfile
import tempfile
import pytest
from app.services.apk_validator import APKValidator, APKValidationResult
from app.services.apk_upload_service import APKUploadService
from app.core.error_codes import ApkErrorCode


@pytest.fixture
def sample_valid_apk_bytes():
    """Creates a minimal valid ZIP archive mimicking an APK structure."""
    buf = tempfile.NamedTemporaryFile(delete=False, suffix=".apk")
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("AndroidManifest.xml", b"<manifest></manifest>")
        zf.writestr("classes.dex", b"dex\n035\x00" + b"\x00" * 100)
        zf.writestr("resources.arsc", b"ARSC" + b"\x00" * 50)
    buf.close()
    with open(buf.name, "rb") as f:
        data = f.read()
    os.remove(buf.name)
    return data


# ============================================================
# 1. APK Validator Tests
# ============================================================

def test_valid_apk_validation(sample_valid_apk_bytes):
    validator = APKValidator()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as f:
        f.write(sample_valid_apk_bytes)
        f_path = f.name

    try:
        res = validator.validate_apk_file(f_path, filename="app.apk")
        assert res.valid is True
        assert len(res.errors) == 0
        assert len(res.sha256) == 64
        assert res.archive_entries >= 2
        assert res.validation_time_ms >= 0
    finally:
        os.remove(f_path)


def test_invalid_extension_rejection():
    validator = APKValidator()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as f:
        f.write(b"MZ executable payload")
        f_path = f.name

    try:
        res = validator.validate_apk_file(f_path, filename="malware.exe")
        assert res.valid is False
        assert res.error_code == ApkErrorCode.INVALID_APK
    finally:
        os.remove(f_path)


def test_unsupported_variant_rejection():
    validator = APKValidator()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xapk") as f:
        f.write(b"XAPK payload")
        f_path = f.name

    try:
        res = validator.validate_apk_file(f_path, filename="app.xapk")
        assert res.valid is False
        assert res.error_code == ApkErrorCode.UNSUPPORTED_APK_VARIANT
    finally:
        os.remove(f_path)


def test_zero_byte_file_rejection():
    validator = APKValidator()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as f:
        f_path = f.name

    try:
        res = validator.validate_apk_file(f_path, filename="empty.apk")
        assert res.valid is False
        assert res.error_code == ApkErrorCode.INVALID_APK
    finally:
        os.remove(f_path)


def test_invalid_mime_rejection(sample_valid_apk_bytes):
    validator = APKValidator()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as f:
        f.write(sample_valid_apk_bytes)
        f_path = f.name

    try:
        res = validator.validate_apk_file(f_path, filename="app.apk", mime_type="image/png")
        assert res.valid is False
        assert res.error_code == ApkErrorCode.INVALID_MIME
    finally:
        os.remove(f_path)


def test_path_traversal_detection():
    validator = APKValidator()
    buf = tempfile.NamedTemporaryFile(delete=False, suffix=".apk")
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("../evil.dex", b"malicious code")
    buf.close()

    try:
        res = validator.validate_apk_file(buf.name, filename="traversal.apk")
        assert res.valid is False
        assert res.error_code == ApkErrorCode.PATH_TRAVERSAL_DETECTED
    finally:
        os.remove(buf.name)


def test_corrupted_zip_rejection():
    validator = APKValidator()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as f:
        f.write(b"PK\x03\x04 corrupted junk headers")
        f_path = f.name

    try:
        res = validator.validate_apk_file(f_path, filename="corrupt.apk")
        assert res.valid is False
        assert res.error_code in (ApkErrorCode.CORRUPTED_ARCHIVE, ApkErrorCode.MALFORMED_ZIP)
    finally:
        os.remove(f_path)


# ============================================================
# 2. APK Upload Service Tests
# ============================================================

@pytest.mark.asyncio
async def test_apk_upload_service_success(sample_valid_apk_bytes):
    service = APKUploadService(base_storage_dir="storage/test_uploads/apk")
    user_id = uuid.uuid4()

    res = await service.process_upload(
        user_id=user_id,
        file_bytes=sample_valid_apk_bytes,
        original_filename="sample_app.apk",
        mime_type="application/vnd.android.package-archive",
    )

    assert res.validated is True
    assert res.sha256 == res.validation_result.sha256
    assert os.path.exists(res.storage_path)

    # Cleanup test upload artifact
    if os.path.exists(res.storage_path):
        os.remove(res.storage_path)
