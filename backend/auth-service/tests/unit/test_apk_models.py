"""Unit tests for SQLAlchemy 2.0 ORM APK Models (Phase 3.7 Part 1A Message 3A)."""

import uuid
import pytest
from app.models.apk_metadata import (
    APKMetadataModel,
    APKPermissionModel,
    APKDEXModel,
    APKNativeLibraryModel,
    APKCertificateModel,
)


def test_apk_models_instantiation():
    scan_id = uuid.uuid4()
    meta = APKMetadataModel(
        scan_id=scan_id,
        package_name="com.truthshield.app",
        version_name="1.0.0",
        version_code=100,
        apk_size=1024000,
        apk_sha256="a" * 64,
    )

    perm = APKPermissionModel(
        apk_id=meta.id,
        permission_name="android.permission.INTERNET",
        declared_by_app=False,
    )

    dex = APKDEXModel(
        apk_id=meta.id,
        filename="classes.dex",
        sha256="b" * 64,
        size=50000,
        class_count=10,
        method_count=50,
    )

    lib = APKNativeLibraryModel(
        apk_id=meta.id,
        library_name="libcrypto.so",
        architecture="arm64-v8a",
        sha256="c" * 64,
        size=200000,
    )

    cert = APKCertificateModel(
        apk_id=meta.id,
        subject="CN=TruthShield",
        issuer="CN=TruthShield",
        sha256="d" * 64,
        self_signed=True,
    )

    assert meta.package_name == "com.truthshield.app"
    assert perm.permission_name == "android.permission.INTERNET"
    assert dex.filename == "classes.dex"
    assert lib.architecture == "arm64-v8a"
    assert cert.self_signed is True
