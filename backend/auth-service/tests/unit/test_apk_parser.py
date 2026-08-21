"""Unit tests for Master APK Parser Engine (Phase 3.7 Part 1A Message 2)."""

import os
import zipfile
import tempfile
import pytest
from app.services.apk_parser import APKParser


@pytest.fixture
def synthetic_apk_path():
    """Creates a synthetic in-memory APK archive containing Manifest, DEX, resources, and native libraries."""
    buf = tempfile.NamedTemporaryFile(delete=False, suffix=".apk")
    xml_manifest = b"""<?xml version="1.0" encoding="utf-8"?>
    <manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.truthshield.test">
        <uses-permission android:name="android.permission.CAMERA" />
        <application android:debuggable="false">
            <activity android:name=".MainActivity" />
        </application>
    </manifest>
    """
    dex_bytes = b"dex\n035\x00" + b"\x00" * 200
    so_bytes = b"\x7fELF" + b"\x00" * 300

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("AndroidManifest.xml", xml_manifest)
        zf.writestr("classes.dex", dex_bytes)
        zf.writestr("classes2.dex", dex_bytes)
        zf.writestr("res/drawable/logo.png", b"PNG_DATA")
        zf.writestr("lib/arm64-v8a/libcrypto.so", so_bytes)
    buf.close()
    yield buf.name
    if os.path.exists(buf.name):
        os.remove(buf.name)


def test_apk_parser_master_flow(synthetic_apk_path):
    parser = APKParser()
    meta = parser.parse_apk_file(synthetic_apk_path)

    assert meta.package_size > 0
    assert len(meta.apk_sha256) == 64
    assert meta.dex_count == 2
    assert meta.native_library_count == 1
    assert meta.resource_count == 1

    assert meta.manifest_metadata is not None
    assert len(meta.manifest_metadata.permissions) == 1
    assert meta.manifest_metadata.permissions[0].name == "android.permission.CAMERA"

    assert meta.dex_summary is not None
    assert meta.dex_summary.total_dex_files == 2

    assert meta.native_library_summary is not None
    assert meta.native_library_summary.library_count == 1

    assert meta.resource_inventory is not None
    assert meta.resource_inventory.image_count == 1
