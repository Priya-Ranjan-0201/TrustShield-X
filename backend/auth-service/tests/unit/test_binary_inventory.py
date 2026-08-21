"""Unit tests for APK Binary Inventory Engine (Phase 3.7 Part 1A.12)."""

import io
import zipfile
import pytest
from app.services.apk_binary_inventory import APKBinaryInventoryService
from app.schemas.apk_binary_inventory_models import FileCategoryEnum


def test_analyze_zip_entries_flow():
    # Build in-memory mock APK ZIP file
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("classes.dex", b"dex\n035\x00data")
        zf.writestr("classes2.dex", b"dex\n035\x00data2")
        zf.writestr("lib/arm64-v8a/libnative.so", b"\x7fELFnativecode")
        zf.writestr("res/drawable/icon.png", b"\x89PNGicon")
        zf.writestr("assets/model.tflite", b"TFL3model")
        zf.writestr("AndroidManifest.xml", b"<manifest></manifest>")

    service = APKBinaryInventoryService()
    result = service.analyze_zip_entries(raw_zip_bytes=buf.getvalue())

    assert result.statistics.total_files == 6
    assert result.statistics.dex_count == 2
    assert result.statistics.native_library_count == 1
    assert result.statistics.resources_count == 1
    assert result.statistics.assets_count == 1
    assert len(result.entries) == 6
