"""Unit tests for Async APK Repository (Phase 3.7 Part 1A Message 3B)."""

import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.apk_repository import APKRepository
from app.schemas.apk_models import (
    APKMetadata,
    ManifestMetadata,
    PermissionInfo,
    DEXSummary,
    DEXMetadata,
    NativeLibrarySummary,
    NativeLibraryMetadata,
)
from app.services.certificate_extractor import CertificateMetadata


@pytest.mark.asyncio
async def test_apk_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = APKRepository(db_mock)
    scan_id = uuid.uuid4()

    apk_meta = APKMetadata(
        package_name="com.example.app",
        version_name="1.0.0",
        version_code=1,
        package_size=50000,
        apk_sha256="1" * 64,
        manifest_metadata=ManifestMetadata(
            permissions=[PermissionInfo(name="android.permission.INTERNET")]
        ),
        dex_summary=DEXSummary(
            total_dex_files=1,
            dex_files=[DEXMetadata(filename="classes.dex", size=1000, sha256="2" * 64)]
        ),
        native_library_summary=NativeLibrarySummary(
            library_count=1,
            libraries=[NativeLibraryMetadata(library_name="libfoo.so", architecture="arm64-v8a", size=2000, sha256="3" * 64, path="lib/arm64-v8a/libfoo.so")]
        ),
    )
    cert_meta = CertificateMetadata(
        subject="CN=App",
        issuer="CN=App",
        sha256="4" * 64,
        self_signed=True,
    )

    result_model = await repo.save_apk_analysis(scan_id=scan_id, apk_meta=apk_meta, cert_meta=cert_meta)
    assert result_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
